#!/usr/bin/env python
# Yannick Dayer <yannick.dayer@idiap.ch>
# Wed 16 Jun 2021 17:21:47 UTC+02

import logging
import os.path

from bob.bio.base.database import CSVDataset
from bob.extension import rc
from bob.extension.download import get_file

logger = logging.getLogger(__name__)


def download_voxforge_data(list_file):
    raise NotImplementedError(
        "VoxForge data download not yet available. Please, download manually."
    )
    logger.info("Downloading data files from VoxForge...")

    logger.info("Download completed.")


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
                os.path.join(dataset_protocol_path, protocol, "list_of_data_files.lst")
            )

        logger.info(
            f"Database: Will read CSV protocol definitions in '{dataset_protocol_path}'."
        )
        logger.info(f"Database: Will read raw data files in '{data_path}'.")
        super().__init__(
            name="VoxForge",
            protocol=protocol,
            dataset_protocol_path=dataset_protocol_path,
            allow_scoring_with_all_biometric_references=True,
            **kwargs,
        )
