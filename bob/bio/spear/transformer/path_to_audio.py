#!/usr/bin/env python
# @author: Yannick Dayer <yannick.dayer@idiap.ch>
# @date: Thu 01 Jul 2021 10:41:55 UTC+02

import logging
from functools import partial
from typing import Optional

from librosa import load as wav_load
from sklearn.base import BaseEstimator, TransformerMixin

from bob.pipelines import DelayedSample

logger = logging.getLogger(__name__)


def load_data_from_file(filename: str, forced_sr: Optional[int] = None):
    logger.debug(f"Reading data from audio file {filename}")
    # Loading the audio file as int16 as bob.ap expects that format (int16 casted to float).
    return wav_load(filename, sr=forced_sr, mono=False, dtype="int16")


def get_audio_sample_rate(sample: DelayedSample, forced_sr: Optional[int] = None):
    """Returns the sample rate of the audio data."""
    return load_data_from_file(sample.data, forced_sr=forced_sr)[1]


def get_audio_data(sample: DelayedSample, forced_sr: Optional[int] = None):
    """Returns the audio data as a numpy array. Returns only mono data.

    If the audio data has more than one channel, the first channel (0) is returned
    unless ``sample`` has a ``channel`` attribute (in which case that channel is
    returned).

    Parameters
    ----------
    sample
        A Sample containing the path to the audio file. Can also specify the audio
        channel number to load.
    forced_sr
        If not None, the audio is resampled to match this value.

    Returns
    -------
    numpy.ndarray of shape (n_audio_samples,)
        The audio data of one channel loaded from the file.
    """
    audio_signal = load_data_from_file(sample.data, forced_sr=forced_sr)[0]

    if audio_signal.ndim > 1:
        channel = sample.channel if hasattr(sample, "channel") else 0
        if audio_signal.shape[0] > 1 and not hasattr(sample, "channel"):
            logger.warning(
                f"audio_signal has {audio_signal.shape[0]} channels and sample.channel "
                f"is not specified. loading only channel 0. ({sample})"
            )
        audio_signal = audio_signal[channel]

    # Converting to float64 as bob.ap expects that format (int16 casted to float).
    return audio_signal.astype(float)


def populate_sample_with_reader(
    sample: DelayedSample, forced_sr: Optional[int] = None
) -> DelayedSample:
    """Assigns the Sample's data and metadata."""


class PathToAudio(BaseEstimator, TransformerMixin):
    """Transforms a Sample's data containing a path to an audio signal.

    The Sample's metadata are updated (rate).

    Note:
        bob.ap expects int16 audio (range [-32768, 32767]), but in float format. Hence
        the loading as int16 and the cast to float. (values will be in the range
        [-32768.0, 32767.0])
    """

    def __init__(self, forced_sr: Optional[int] = None) -> None:
        """
        Parameters
        ----------
        forced_sr
            If not None, every sample rate will be forced to this value (resampling if
            needed).
        """
        super().__init__()
        self.forced_sr = forced_sr

    def transform(self, samples: list):
        output_samples = []
        for sample in samples:
            delayed_attrs = {
                "rate": partial(get_audio_sample_rate, sample, self.forced_sr)
            }
            new_sample = DelayedSample(
                load=partial(get_audio_data, sample, self.forced_sr),
                parent=sample,
                delayed_attributes=delayed_attrs,
            )
            output_samples.append(new_sample)
        return output_samples

    def fit(self, X, y=None):
        return self

    def _more_tags(self):
        return {
            "stateless": True,
            "requires_fit": False,
        }
