#!/usr/bin/env python
# @author: Yannick Dayer <yannick.dayer@idiap.ch>
# @date: Thu 01 Jul 2021 10:41:55 UTC+02

import logging

from functools import partial
from typing import Optional

import numpy

from sklearn.base import BaseEstimator, TransformerMixin

from bob.bio.spear.audio_processing import read as read_audio
from bob.pipelines import DelayedSample

logger = logging.getLogger(__name__)


def get_audio_sample_rate(path: str, forced_sr: Optional[int] = None) -> int:
    """Returns the sample rate of the audio data."""
    return (
        forced_sr if forced_sr is not None else read_audio(path, None, None)[1]
    )


def get_audio_data(
    path: str,
    channel: Optional[int] = None,
    forced_sr: Optional[int] = None,
) -> numpy.ndarray:
    """Returns the audio data from the given path."""
    return read_audio(path, channel, forced_sr)[0]


class PathToAudio(BaseEstimator, TransformerMixin):
    """Transforms a Sample's data containing a path to an audio signal.

    The Sample's metadata are updated (rate).

    Note:
        audio processing functions expect int16 audio (range [-32768, 32767]), but in
        float format. Hence the loading as int16 and the cast to float. (values will be
        in the range [-32768.0, 32767.0])
    """

    def __init__(
        self,
        forced_channel: Optional[int] = None,
        forced_sr: Optional[int] = None,
    ) -> None:
        """
        Parameters
        ----------
        forced_sr:
            If not None, every sample rate will be forced to this value (resampling if
            needed).
        forced_channel:
            Forces the loading of a specific channel for each audio file, if the samples
            don't have a ``channel`` attribute. If None and the samples don't have a
            ``channel`` attribute, all the channels will be loaded in a 2D array.
        """
        super().__init__()
        self.forced_channel = forced_channel
        self.forced_sr = forced_sr

    def transform(self, samples: list) -> list:
        output_samples = []
        for sample in samples:
            channel = getattr(sample, "channel", self.forced_channel)
            load_fn = partial(
                get_audio_data,
                sample.data,
                int(channel) if channel is not None else None,
                self.forced_sr,
            )
            delayed_attrs = {
                "rate": partial(
                    get_audio_sample_rate, sample.data, self.forced_sr
                )
            }
            new_sample = DelayedSample(
                load=load_fn,
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
