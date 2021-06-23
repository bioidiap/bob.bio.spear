#!/usr/bin/env python
# @author: Yannick Dayer <yannick.dayer@idiap.ch>
# Tue 22 Jun 2021 14:53:03 UTC+02

import csv
import logging

from pathlib import Path

import click

from tqdm import tqdm

from bob.bio.spear.database.voxforge import get_voxforge_protocol_file
from bob.extension.download import download_and_unzip
from bob.extension.download import search_file
from bob.extension.scripts.click_helper import verbosity_option

logger = logging.getLogger(__name__)


@click.command(
    epilog="""Examples:

\b
    $ bob db download-voxforge --list-file my_urls.csv --destination my_datasets/data/

The file list can be in a tar archive:

\b
    $ bob db download-voxforge --list-file voxforge.tar.gz:Default/data_files_urls.csv
""",
)
@click.option(
    "--list-file",
    "-l",
    default=None,
    help=(
        "A path to a text file with one line per file to download. "
        "Can be in a tar file: use a ``:`` to point inside the archive. "
        "If ``--list-file`` is omitted, will look for the protocol definition file in "
        "``bob_data_folder``, and download the file from "
        "`https://www.idiap.ch/software/bob/data/bob/bob.bio.spear` if needed."
    ),
)
@click.option(
    "--destination",
    "-d",
    default=None,
    help=(
        "Where to store the downloaded data files. "
        "If omitted, will download to the bob_data/data folder."
    ),
)
@click.option(
    "--force-download",
    "-f",
    is_flag=True,
    help=("Download a file even if it already exists locally."),
)
@verbosity_option()
def download_voxforge(list_file, destination, force_download, verbose, **kwargs):
    """Downloads a series of VoxForge data files from their repository and untar them.

    The files will be downloaded and saved in the `destination` folder then extracted.

    A list of files is required in the form of a csv file with a ``url`` column as well
    as a ``filename`` column that specifies the local name of the file. If the csv file
    is not specified as ``--list-file`` option, it will be looked up in
    ``bob_data_folder`` (see
    :py:func:`bob.bio.spear.database.voxforge.get_voxforge_protocol_file`).
    """
    # logger.setLevel(["ERROR", "WARNING", "INFO", "DEBUG"][verbose])

    destination = Path(destination)
    destination.mkdir(exist_ok=True)

    # Defaults to list in protocol definition
    if list_file is None:
        protocol_file = get_voxforge_protocol_file()
        list_file = f"{protocol_file}:Default/data_files_urls.csv"

    # Open the list file
    if ":" in list_file:
        tar_base, in_file = list_file.split(":", maxsplit=1)
        open_list_file = search_file(tar_base, [in_file])  # Returns an open file
    else:
        open_list_file = open(list_file, "r")

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

    logger.info(f"Download of {num_files} completed.")
    open_list_file.close()
