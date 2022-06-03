#!/usr/bin/env python
# @author: Yannick Dayer <yannick.dayer@idiap.ch>
# @date: Wed 25 May 2022 17:27:31 UTC+02

import logging

from typing import List, Optional

import numpy

from sklearn.base import BaseEstimator, TransformerMixin

from bob.bio.spear.audio_processing import resample

logger = logging.getLogger(__name__)


class Resample(BaseEstimator, TransformerMixin):
    """Transforms a Sample's audio data with a new sample rate."""

    def __init__(self, target_sample_rate: Optional[int] = None) -> None:
        """
        Parameters
        ----------
        target_sample_rate:
            The target sample rate for the audio output.
        """
        super().__init__()
        self.target_sample_rate = target_sample_rate

    def transform(
        self, audio_streams: List[numpy.ndarray], sample_rates: List[int]
    ) -> List[numpy.ndarray]:
        output = []
        for audio, sample_rate in zip(audio_streams, sample_rates):
            output.append(resample(audio, sample_rate, self.target_sample_rate))
        return output

    def fit(self, X, y=None):
        return self

    def _more_tags(self):
        return {
            "stateless": True,
            "requires_fit": False,
            "bob_transform_extra_input": [("sample_rates", "rate")],
        }  # TODO: add multi-output tag
