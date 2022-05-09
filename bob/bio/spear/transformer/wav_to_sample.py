#!/usr/bin/env python
# @author: Yannick Dayer <yannick.dayer@idiap.ch>
# @date: Thu 01 Jul 2021 10:41:55 UTC+02

import logging

from functools import partial

from scipy.io import wavfile
from sklearn.base import BaseEstimator, TransformerMixin

from bob.pipelines import DelayedSample

logger = logging.getLogger(__name__)


def load_data_from_file(filename: str):
    logger.debug(f"Reading data from audio file {filename}")
    rate, wav_samples = wavfile.read(filename)
    return rate, wav_samples


def get_audio_sample_rate(sample):
    return load_data_from_file(sample.data)[0]


def get_audio_data(sample):
    audio_signal = load_data_from_file(sample.data)[1]

    if audio_signal.ndim > 1:
        if audio_signal.shape[0] > 1:
            logger.warning(
                f"audio_signal has {audio_signal.shape[0]} channels. Returning only "
                "channel 0."
            )
        audio_signal = audio_signal[0]

    return audio_signal.astype(float)


class WavToSample(BaseEstimator, TransformerMixin):
    """Transforms a Sample's data containing a path to an audio signal.

    The Sample's metadata are updated.
    """

    def populate_from_reader(self, sample: DelayedSample) -> DelayedSample:
        """Assigns the Sample's data and metadata."""
        delayed_attr = {"rate": partial(get_audio_sample_rate, sample)}
        new_sample = DelayedSample(
            load=partial(get_audio_data, sample),
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
            "requires_fit": False,
        }
