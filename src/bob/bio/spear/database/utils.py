import logging

from typing import Union

from clapper.rc import UserDefaults
from sklearn.pipeline import Pipeline

from bob.bio.base.database import AnnotationsLoader, FileSampleLoader
from bob.bio.spear.transformer import PathToAudio

logger = logging.getLogger(__name__)

_common_rc = UserDefaults("~/.bobrc")


def get_rc():
    return _common_rc


def path_loader(path: str):
    logger.debug("Reading CSV row for %s", path)
    return path


def create_sample_loader(
    data_path: Union[str, None] = None,
    data_ext: str = ".wav",
    annotations_path: Union[str, None] = None,
    annotations_ext: str = ".json",
    force_sample_rate: Union[int, None] = None,
    force_channel: Union[int, None] = None,
):
    """Defines the data loading transformers"""

    # Load a path into the data of the sample
    sample_loader = FileSampleLoader(
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

    return sample_loader
