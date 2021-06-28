#!/usr/bin/env python
# @author: Yannick Dayer <yannick.dayer@idiap.ch>
# @date: Wed 16 Jun 2021 17:21:47 UTC+02

import csv
import logging

from pathlib import Path

import click

from tqdm import tqdm

import bob.io.base

from bob.bio.base.database import CSVDataset
from bob.bio.base.database import CSVToSampleLoaderBiometrics
from bob.extension import rc
from bob.extension.download import download_and_unzip
from bob.extension.download import get_file
from bob.extension.download import search_file
from bob.extension.scripts.click_helper import verbosity_option

logger = logging.getLogger(__name__)


def get_voxforge_protocol_file():
    """Returns the protocol definition archive, downloading it if necessary.

    Looks into ``bob_data_folder``, into the ``datasets`` folder for the file, and
    download it from https://www.idiap.ch/software/bob/data/bob/bob.bio.spear/ if
    needed.
    """
    proto_def_hash = "dc84ac65"
    proto_def_name = f"database-protocols-voxforge-{proto_def_hash}.tar.gz"
    proto_def_urls = [
        f"https://www.idiap.ch/software/bob/data/bob/bob.bio.spear/{proto_def_name}",
        f"http://www.idiap.ch/software/bob/data/bob/bob.bio.spear/{proto_def_name}",
    ]
    logger.info(f"Retrieving protocol definition file '{proto_def_name}'.")
    return get_file(
        filename=proto_def_name,
        urls=proto_def_urls,
        file_hash=proto_def_hash,
        cache_subdir="datasets",
    )


def VoxforgeBioDatabase(
    protocol="Default", dataset_protocol_path=None, data_path=None, **kwargs
):
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

    Although not provided by bob, the VoxForge data is freely available online.
    If you don't already have the data, download it and set the bob configuration using
    the following commands:

    ``$ bob db download-voxforge -d your_path_to_data``

    ``$ bob config set bob.db.voxforge.directory your_path_to_data``


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
    """

    if dataset_protocol_path is None:
        dataset_protocol_path = get_voxforge_protocol_file()

    if data_path is None:
        data_path = rc.get("bob.db.voxforge.directory")
    if data_path is None:
        logger.warning(
            "No data path was provided! Either set "
            "'bob.db.voxforge.directory' with the 'bob config set' command, or "
            "provide a 'data_path' to VoxforgeBioDatabase."
        )

    logger.info(
        f"Database: Will read the CSV protocol definitions in '{dataset_protocol_path}'."
    )
    logger.info(f"Database: Will read raw data files in '{data_path}'.")
    return CSVDataset(
        name="VoxForge",
        protocol=protocol,
        dataset_protocol_path=dataset_protocol_path,
        csv_to_sample_loader=CSVToSampleLoaderBiometrics(
            data_loader=bob.io.base.load,
            dataset_original_directory=data_path,
            extension=".wav",
        ),
        allow_scoring_with_all_biometric_references=True,
        **kwargs,
    )


@click.command(
    epilog="""Examples:

\b
    $ bob db download-voxforge ./data/

\b
    $ bob db download-voxforge --protocol-definition bio-spear-voxforge.tar ./data/

""",
)
@click.option(
    "--protocol-definition",
    "-p",
    default=None,
    help=(
        "A path to a the protocol definition file of VoxForge. "
        "If omitted, will use the default protocol definition file at "
        "`https://www.idiap.ch/software/bob/data/bob/bob.bio.spear`."
    ),
)
@click.option(
    "--force-download",
    "-f",
    is_flag=True,
    help="Download a file even if it already exists locally.",
)
@click.argument("destination")
@verbosity_option()
def download_voxforge(protocol_definition, destination, force_download, **kwargs):
    """Downloads a series of VoxForge data files from their repository and untar them.

    The files will be downloaded and saved in the `destination` folder then extracted.

    The list of URLs is provided in the protocol definition file of Voxforge.
    """

    destination = Path(destination)
    destination.mkdir(exist_ok=True)

    if protocol_definition is None:
        protocol_definition = get_voxforge_protocol_file()

    # Use the `Default` protocol
    protocol = "Default"

    # Open the list file
    list_file = f"{protocol}/data_files_urls.csv"
    open_list_file = search_file(protocol_definition, [list_file])

    num_files = sum(1 for _ in open_list_file) - 1
    open_list_file.seek(0, 0)
    logger.info(f"{num_files} files are listed in {list_file}. Downloading...")

    csv_list_file = csv.DictReader(open_list_file)

    for row in tqdm(csv_list_file, total=num_files):
        full_filename = destination / row["filename"]
        if force_download or not full_filename.exists():
            logger.debug(f"Downloading {row['filename']} from {row['url']}")
            download_and_unzip(urls=[row["url"]], filename=full_filename)
            logger.debug(f"Downloaded to {full_filename}")

    logger.info(f"Download of {num_files} files completed.")
    open_list_file.close()
