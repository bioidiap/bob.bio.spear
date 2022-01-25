#!/usr/bin/env python

import logging

from sklearn.pipeline import Pipeline

from bob.bio.base.database import CSVDataset
from bob.bio.base.database import CSVToSampleLoaderBiometrics
from bob.bio.spear.transformer import AudioReaderToSample
from bob.extension import rc

logger = logging.getLogger(__name__)


def path_loader(path):
    logger.debug(f"Reading CSV row for {path}")
    return path


def MobioBioDatabase(
    # protocol="male",
    dataset_protocol_path=None,
    gender="male",
    data_path=None,
    annotations_path=None,
    **kwargs,
):
    """Database interface for the Mobio dataset subset for speaker recognition.

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

    annotations_path: str or None
        Path to the annotations of VoxForge if available.
        If None: will not load any annotations.
    """

    if dataset_protocol_path is None:
        dataset_protocol_path = (
            rc.get("bob_data_folder")
            + f"/datasets/database-protocols-mobio-{gender}.tar.gz"
        )

    if data_path is None:
        data_path = rc.get("bob.db.mobio.audio.directory")
    if data_path is None:
        raise RuntimeError(
            "No data path was provided! Either set 'bob.db.mobio.audio.directory' with "
            "the 'bob config set' command, or provide a 'data_path' to "
            "'VoxforgeBioDatabase'."
        )

    logger.info(
        f"Database: Will read the CSV protocol definitions in '{dataset_protocol_path}'."
    )
    logger.info(f"Database: Will read raw data files in '{data_path}'.")

    # Define the data loading transformers

    # Loads an AudioReader object from a wav file
    path_to_data_loader = CSVToSampleLoaderBiometrics(
        data_loader=path_loader,
        dataset_original_directory=data_path,
        extension=".wav",
    )

    # Reads the AudioReader and set the data and metadata of a sample
    reader_to_sample = AudioReaderToSample()

    # Build the data loading pipeline
    sample_loader = Pipeline(
        [
            ("db:reader_loader", path_to_data_loader),
            ("db:reader_to_sample", reader_to_sample),
        ]
    )

    return CSVDataset(
        name=f"mobio-{gender}",
        protocol=gender,
        dataset_protocol_path=dataset_protocol_path,
        csv_to_sample_loader=sample_loader,
        allow_scoring_with_all_biometric_references=True,
        **kwargs,
    )
