#!/usr/bin/env python
# @author: Yannick Dayer <yannick.dayer@idiap.ch>
# @date: Thu 01 Jul 2021 10:41:55 UTC+02

import logging

from functools import lru_cache
from functools import partial

from sklearn.base import BaseEstimator
from sklearn.base import TransformerMixin

from bob.io.audio import reader as AudioReader
from bob.pipelines import DelayedSample

logger = logging.getLogger(__name__)


audio_reader_keys = [
    "rate",
    "number_of_samples",
    "number_of_channels",
    "bits_per_sample",
    "duration",
    "encoding",
    "type",
    "compression_factor",
]


@lru_cache()
def load_metadata_from_file(filename: str):
    """Extracts data and a set of metadata from a reader object."""
    logger.debug(f"Reading metadata from audio file {filename}")

    reader = AudioReader(filename)
    return {key: getattr(reader, key) for key in audio_reader_keys}


def load_data_from_file(filename: str):
    logger.debug(f"Reading data from audio file {filename}")
    reader = AudioReader(filename)
    return reader.load()


def get_audio_attribute(sample, key):
    if key == "data":
        return load_data_from_file(sample.data)
    return load_metadata_from_file(sample.data)[key]


class AudioReaderToSample(BaseEstimator, TransformerMixin):
    """Transforms a Sample's data containing a path to an audio signal.

    The Sample's metadata are updated.
    """

    def populate_from_reader(self, sample: DelayedSample) -> DelayedSample:
        """Assigns the Sample's data and metadata."""
        delayed_attr = {
            key: partial(get_audio_attribute, sample, key) for key in audio_reader_keys
        }
        new_sample = DelayedSample(
            load=partial(get_audio_attribute, sample, "data"),
            parent=sample,
            delayed_attributes=delayed_attr,
        )
        return new_sample

    def transform(self, samples: list):
        output = []
        for sample in samples:
            output.append(self.populate_from_reader(sample))
        return output

    def fit(self, X, y=None, **fit_params):
        return self

    def _more_tags(self):
        return {
            "stateless": True,
            "requires_fit": False,
        }
