#!/usr/bin/env python
# Yannick Dayer <yannick.dayer@idiap.ch>
# Wed 16 Jun 2021 17:21:47 UTC+02

import logging
import os

from tqdm import tqdm

from bob.bio.base.database import CSVDataset
from bob.extension import rc
from bob.extension.download import get_file
from bob.extension.download import search_file

logger = logging.getLogger(__name__)


def download_voxforge_data(list_file: str):
    """Downloads a series of VoxForge data files from their repository and untar them.

    The files will be retrieved by :py:func:`bob.extension.download.get_file` and saved
    in the ``data/voxforge`` subdirectory of `bob_data_folder`.

    Parameters
    ----------

    list_file: str
        A path to a text file with one line per file to download.
    """
    if ":" in list_file:
        tar_base, in_file = list_file.split(":", maxsplit=1)
        list_file = search_file(tar_base, [in_file])  # Returns an open file
    else:
        list_file = open(list_file, "r")

    voxforge_repo = "http://www.repository.voxforge1.org"
    base_url = f"{voxforge_repo}/downloads/SpeechCorpus/Trunk/Audio/Main/16kHz_16bit"
    num_files = sum(1 for _ in list_file)
    list_file.seek(0, 0)
    if num_files > 20:
        logger.warning(f"Downloading {num_files} will take some time.")
    logger.info(
        f"{num_files} files are listed in {list_file}. Downloading from {base_url}..."
    )
    for line in tqdm(list_file, total=num_files):
        tar_file = line.strip()
        file_name = os.path.basename(tar_file)
        data_file_url = f"{base_url}/{tar_file}"
        logger.debug(f"Downloading {file_name} from {data_file_url}")
        final_file = get_file(
            filename=file_name,
            urls=[data_file_url],
            cache_subdir=os.path.join("data", "voxforge"),
            extract=True,
            force=False,
        )
        logger.debug(f"Downloaded to {final_file}")
    logger.info(f"Download of {num_files} completed.")
    list_file.close()


class VoxforgeBioDatabase(CSVDataset):
    """Database interface for the VoxForge dataset subset for speaker recognition.

    This database interface is meant to be used with the vanilla-biometrics pipeline.

    Given a series of CSV files (or downloading them from the bob data server), it
    creates the Sample objects for each roles needed by the pipeline (enroll, probe),
    for different groups (dev, eval).

    `protocol definition` files are not the `data` files:
        - `protocol definition` files are a list of paths and corresponding reference
            name. They are available on the bob data server.
        - `data` files are the actual files of the dataset (pointed to by the definition
            files). They are not provided by bob.

    The VoxForge data is freely available online. It is possible to automatically
    download the list of necessary files.

    Used bob config variables (set with ``bob config``):
        - ``bob_data_folder``
        - ``bob.db.voxforge.directory``

    Parameters
    ----------

    protocol: str
        Name of the protocol to use (subfolder in protocol definition).

    dataset_protocol_path: str or None
        Path to an existing protocol definition folder structure.
        If None: will download the definition files to the path pointed by the
        ``bob_data_folder`` config (see :py:func:`bob.extension.download.get_file`).

    data_path: str or None
        Path to the data files of VoxForge.
        If None: will use the path in the ``bob.db.voxforge.directory`` config.
        If None and the config is not set: will download the files to the bob data
        folder.
    """

    def __init__(self, protocol, dataset_protocol_path=None, data_path=None, **kwargs):
        if dataset_protocol_path is None:
            proto_def_hash = "xxxxxxxx"  # TODO bob dav
            proto_def_name = f"bio-spear-voxforge-{proto_def_hash}.tar.gz"
            proto_def_urls = [
                f"https://www.idiap.ch/software/bob/data/bob/bob.bio.spear/{proto_def_name}",
                f"http://www.idiap.ch/software/bob/data/bob/bob.bio.spear/{proto_def_name}",
            ]
            dataset_protocol_path = get_file(
                filename=proto_def_name,
                urls=proto_def_urls,
                file_hash=proto_def_hash,
                cache_subdir="datasets",
            )

        if data_path is None:
            data_path = rc.get("bob.db.voxforge.directory", None)
        if data_path is None:
            # Download and extract the files specified in dataset definition
            bob_data_path = rc.get(
                "bob_data_folder", os.path.join(os.path.expanduser("~"), "bob_data")
            )
            data_path = os.path.join(bob_data_path, "data")
            download_voxforge_data(
                f"{dataset_protocol_path}:{protocol}/list_of_data_files.lst"
            )

        logger.info(
            f"Database: Will read the CSV protocol definitions in '{dataset_protocol_path}'."
        )
        logger.info(f"Database: Will read raw data files in '{data_path}'.")
        super().__init__(
            name="VoxForge",
            protocol=protocol,
            dataset_protocol_path=dataset_protocol_path,
            allow_scoring_with_all_biometric_references=True,
            **kwargs,
        )
