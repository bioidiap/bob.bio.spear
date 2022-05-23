#!/usr/bin/env python
# Yannick Dayer <yannick.dayer@idiap.ch>
# Wed 16 Mar 2022 09:32:47 UTC+01

import logging

from typing import Union

from sklearn.pipeline import Pipeline

from bob.bio.base.database import CSVDataset, CSVToSampleLoaderBiometrics
from bob.bio.spear.transformer import PathToAudio
from bob.extension import rc
from bob.extension.download import get_file
from bob.pipelines.sample_loaders import AnnotationsLoader

logger = logging.getLogger(__name__)


known_databases = {
    "voxforge": {
        "definition_file": "database-protocols-voxforge-f032929d.tar.gz",
        "crc": "f032929d",
    },
    "mobio": {
        "definition_file": "database-protocols-mobio-e069c6aa.tar.gz",
        "crc": "e069c6aa",
        "rc_name": "mobio.audio",
    },
    "timit": {
        "definition_file": "database-protocols-timit-1f14a1b4.tar.gz",
        "crc": "1f14a1b4",
    },
    "avspoof": {
        "definition_file": "database-protocols-avspoof-109c8110.tar.gz",
        "crc": "109c8110",
    },
    "asvspoof": {
        "definition_file": "database-protocols-asvspoof-e96b5728.tar.gz",
        "crc": "e96b5728",
    },
    "asvspoof2017": {
        "definition_file": "database-protocols-asvspoof2017-db087bb7.tar.gz",
        "crc": "db087bb7",
    },
    "voicepa": {
        "definition_file": "database-protocols-voicepa-25ce140b.tar.gz",
        "crc": "25ce140b",
    },
    "nist_sre04to16": {
        "definition_file": "database-protocols-nist_sre04to16-8aea7733.tar.gz",
        "crc": "8aea7733",
    },
}


def get_protocol_file(database_name: str):
    """Returns the protocol definition archive, downloading it if necessary.

    Looks for the file into ``bob_data_folder``, into the ``datasets`` folder, and
    downloads it from https://www.idiap.ch/software/bob/data/bob/bob.bio.spear/ if
    needed.
    """
    if database_name not in known_databases:
        raise ValueError(
            f"The provided database '{database_name}' name is unknown. Use one of "
            f"{known_databases.keys()} or specify a dataset_protocol_path to "
            "'SpearBioDatabase'."
        )
    proto_def_hash = known_databases[database_name]["crc"]
    proto_def_name = known_databases[database_name]["definition_file"]
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


def path_loader(path: str):
    logger.debug(f"Reading CSV row for {path}")
    return path


def SpearBioDatabase(
    name: str,
    protocol: Union[str, None] = None,
    dataset_protocol_path: Union[str, None] = None,
    data_path: Union[str, None] = None,
    data_ext: str = ".wav",
    annotations_path: Union[str, None] = None,
    annotations_ext: str = ".json",
    force_sample_rate: Union[int, None] = None,
    force_channel: Union[int, None] = None,
    **kwargs,
):
    """Database interface for the bob.bio.spear datasets for speaker recognition.

    This database interface is meant to be used with bob.bio.base pipelines.

    Given a series of CSV files (or downloading them from the bob data server), it
    creates the Sample objects for each roles needed by the pipeline (enroll, probe),
    for different groups (train, dev, eval).

    Each sample contains:

        - `data`: the wav audio data,
        - `rate`: the sample rate of `data`,
        - (optional)`annotations`: some annotations loaded from files if
          `annotations_path` is provided.

    `protocol definition` files (CSV files) are not the `data` files (WAV files):

        - `protocol definition` files are a list of paths and corresponding reference
          name. They are available on the bob data server.
        - `data` files are the actual files of the dataset (pointed to by the definition
          files). They are not provided by bob.

    You have to set the bob configuration to the root folder of the data files using
    the following command:

    ``$ bob config set bob.db.<database_name>.directory <your_path_to_data>``

    The final data paths will be constructed with the bob.db.<database_name>.directory
    key, and the paths in the CSV protocol definition files.

    Parameters
    ----------

    name
        name of the database used for retrieving config keys and files.

    protocol
        protocol to use (sub-folder containing the protocol definition files).

    dataset_protocol_path
        Path to an existing protocol definition folder structure.
        If None: will download the definition files to a datasets folder in the path
        pointed by the ``bob_data_folder`` config (see
        :py:func:`bob.extension.download.get_file`).

    data_path
        Path to the data files of the database.
        If None: will use the path in the ``bob.db.<database_name>.directory`` config.

    data_ext
        File extension of the data files.

    annotations_path
        Path to the annotations files of the dataset, if available.
        If None: will not load any annotations (you could then annotate on the fly with
        a transformer).

    annotations_ext
        If annotations_path is provided, will load annotation using this extension.

    force_sample_rate
        If not None, will force the sample rate of the data to a specific value.
        Otherwise the sample rate will be specified by each loaded file.

    force_channel
        If not None, will force to load the nth channel of each file. If None and the
        samples have a ``channel`` attribute, this channel will be loaded, and
        otherwise all channels will be loaded in a 2D array if multiple are present.
    """

    if dataset_protocol_path is None:
        dataset_protocol_path = get_protocol_file(name)

    logger.info(
        f"Database: Will read the CSV protocol definitions in '{dataset_protocol_path}'."
    )

    rc_db_name = known_databases.get(name, {}).get("rc_name", name)

    if data_path is None:
        data_path = rc.get(f"bob.db.{rc_db_name}.directory")
    if data_path is None:
        raise RuntimeError(
            f"No data path was provided! Either set 'bob.db.{rc_db_name}.directory' "
            "with the 'bob config set' command, or provide a 'data_path' to "
            "'SpearBioDatabase'."
        )

    logger.info(f"Database: Will read raw data files in '{data_path}'.")

    # Define the data loading transformers

    # Load a path into the data of the sample
    sample_loader = CSVToSampleLoaderBiometrics(
        data_loader=path_loader,
        dataset_original_directory=data_path,
        extension=data_ext,
    )

    # Read the file at path and set the data and metadata of a sample
    path_to_sample = PathToAudio(
        forced_channel=force_channel, forced_sr=force_sample_rate
    )

    # Build the data loading pipeline
    if annotations_path is None:
        sample_loader = Pipeline(
            [
                ("db:reader_loader", sample_loader),
                ("db:path_to_sample", path_to_sample),
            ]
        )
    else:
        logger.info(
            f"Database: Will read annotation files in '{annotations_path}'."
        )
        annotations_transformer = AnnotationsLoader(
            annotation_directory=annotations_path,
            annotation_extension=annotations_ext,
        )
        sample_loader = Pipeline(
            [
                ("db:reader_loader", sample_loader),
                ("db:path_to_sample", path_to_sample),
                ("db:annotations_loader", annotations_transformer),
            ]
        )

    return CSVDataset(
        name=name,
        protocol=protocol,
        dataset_protocol_path=dataset_protocol_path,
        csv_to_sample_loader=sample_loader,
        score_all_vs_all=True,
        **kwargs,
    )
