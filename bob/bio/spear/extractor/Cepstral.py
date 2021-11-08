#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Elie Khoury <Elie.Khoury@idiap.ch>
# Tue  9 Jun 23:10:43 CEST 2015
#
# Copyright (C) 2012-2013 Idiap Research Institute, Martigny, Switzerland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Cepstral Features for speaker recognition"""

import logging

import numpy

from sklearn.base import BaseEstimator
from sklearn.base import TransformerMixin

import bob.ap

from .. import utils

logger = logging.getLogger(__name__)


class Cepstral(BaseEstimator, TransformerMixin):
    """Extracts the Cepstral features of audio wav data.

    Use a SampleWrapper to use with bob pipelines to pass the `rate` and `annotations`
    attributes to the arguments of `transform`:
    >>> wrap(
    ...     ["sample"],
    ...     Cepstral(),
    ...     transform_extra_arguments=[
    ...         ("sample_rate", "rate"), ("vad_labels", "annotations")
    ...     ]
    ... )
    """

    def __init__(
        self,
        win_length_ms=20,
        win_shift_ms=10,
        n_filters=24,
        dct_norm=False,
        f_min=0.0,
        f_max=4000,
        delta_win=2,
        mel_scale=True,
        with_energy=True,
        with_delta=True,
        with_delta_delta=True,
        n_ceps=19,  # 0-->18
        pre_emphasis_coef=0.95,
        features_mask=None,
        # Normalization
        normalize_flag=True,
        **kwargs,
    ):
        super().__init__(**kwargs)
        # copy parameters
        self.win_length_ms = win_length_ms
        self.win_shift_ms = win_shift_ms
        self.n_filters = n_filters
        self.dct_norm = dct_norm
        self.f_min = f_min
        self.f_max = f_max
        self.delta_win = delta_win
        self.mel_scale = mel_scale
        self.with_energy = with_energy
        self.with_delta = with_delta
        self.with_delta_delta = with_delta_delta
        self.n_ceps = n_ceps
        self.pre_emphasis_coef = pre_emphasis_coef
        self.features_mask = features_mask
        self.normalize_flag = normalize_flag

    def normalize_features(self, params):
        if len(params) == 1:
            # if there is only 1 frame, we cannot normalize it
            return params
        # normalized_vector is mean std normalized version of params per feature dimension
        normalized_vector = (params - params.mean(axis=0)) / params.std(axis=0)
        return normalized_vector

        # normalized_vector = [
        #     [0 for i in range(params.shape[1])] for j in range(params.shape[0])
        # ]
        # for index in range(params.shape[1]):
        #     vector = numpy.array([row[index] for row in params])
        #     n_samples = len(vector)
        #     norm_vector = utils.normalize_std_array(vector)

        #     for i in range(n_samples):
        #         normalized_vector[i][index] = numpy.asscalar(norm_vector[i])
        # data = numpy.array(normalized_vector)
        # return data

    def transform_one(
        self, wav_data: numpy.ndarray, sample_rate: float, vad_labels: numpy.ndarray
    ):
        """Computes and returns normalized cepstral features for the given input data"""
        logger.debug("Cepstral transform.")

        if wav_data.ndim > 1:
            if wav_data.shape[0] > 1:
                logger.warning(
                    "Cepstral Transformer only supports 1 channel data and a sample "
                    f"contains {wav_data.shape[0]}. Will only consider one channel."
                )
            wav_data = wav_data[0]

        # Set parameters
        wl = self.win_length_ms
        ws = self.win_shift_ms
        nf = self.n_filters
        nc = self.n_ceps
        f_min = self.f_min
        f_max = self.f_max
        dw = self.delta_win
        pre = self.pre_emphasis_coef

        ceps = bob.ap.Ceps(sample_rate, wl, ws, nf, nc, f_min, f_max, dw, pre)
        ceps.dct_norm = self.dct_norm
        ceps.mel_scale = self.mel_scale
        ceps.with_energy = self.with_energy
        ceps.with_delta = self.with_delta
        ceps.with_delta_delta = self.with_delta_delta

        cepstral_features = ceps(wav_data)
        if self.features_mask is None:
            features_mask = numpy.arange(0, 60)
        else:
            features_mask = self.features_mask
        if vad_labels is not None:  # don't apply VAD
            filtered_features = cepstral_features[vad_labels == 1]
            # filtered_features = numpy.ndarray(
            #     shape=(sum(vad_labels), len(features_mask)),
            #     dtype=numpy.float64,
            # )
            # i = 0
            # cur_i = 0
            # for row in cepstral_features:
            #     if i < len(vad_labels):
            #         if vad_labels[i] == 1:
            #             for k, mask in enumerate(features_mask):
            #                 filtered_features[cur_i, k] = row[mask]
            #             cur_i = cur_i + 1
            #         i = i + 1
            #     else:
            #         if vad_labels[-1] == 1:
            #             if cur_i == cepstral_features.shape[0]:
            #                 for k, mask in enumerate(features_mask):
            #                     filtered_features[cur_i, k] = row[mask]
            #                 cur_i = cur_i + 1
            #         i = i + 1
        else:
            filtered_features = cepstral_features

        if self.normalize_flag:
            normalized_features = self.normalize_features(filtered_features)
        else:
            normalized_features = filtered_features
        if normalized_features.shape[0] == 0:
            logger.warning("No speech found for this utterance")
            # But do not keep it empty!!! This avoids errors in next steps
            normalized_features = numpy.array([numpy.zeros(len(features_mask))])
        return normalized_features

    def transform(
        self,
        wav_data_set: "list[numpy.ndarray]",
        sample_rate: "list[float]",
        vad_labels: "list[numpy.ndarray]",
    ):
        results = []
        for wav_data, rate, annotations in zip(wav_data_set, sample_rate, vad_labels):
            results.append(self.transform_one(wav_data, rate, annotations))
        return results

    def fit(self, X, y=None, **fit_params):
        return self

    def _more_tags(self):
        return {
            "stateless": True,
            "requires_fit": False,
        }
