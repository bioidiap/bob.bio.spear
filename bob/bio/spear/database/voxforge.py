#!/usr/bin/env python
# @author: Yannick Dayer <yannick.dayer@idiap.ch>
# @date: Wed 16 Jun 2021 17:21:47 UTC+02

import csv
import logging

from pathlib import Path

import click

from tqdm import tqdm

from bob.bio.spear.database.database import get_protocol_file
from bob.extension.download import download_and_unzip, search_file
from bob.extension.scripts.click_helper import verbosity_option

logger = logging.getLogger(__name__)


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
def download_voxforge(
    protocol_definition, destination, force_download, **kwargs
):
    """Downloads a series of VoxForge data files from their repository and untar them.

    The files will be downloaded and saved in the `destination` folder then extracted.

    The list of URLs is provided in the protocol definition file of Voxforge.
    """

    destination = Path(destination)
    destination.mkdir(exist_ok=True)

    if protocol_definition is None:
        protocol_definition = get_protocol_file("voxforge")

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
