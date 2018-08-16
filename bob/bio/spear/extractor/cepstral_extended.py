#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Pavel Korshunov <pavel.korshunov@idiap.ch>
# Fri 6 Nov 17:13:22 CEST 2015
#
# Copyright (C) 2011-2012 Idiap Research Institute, Martigny, Switzerland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from __future__ import print_function

import numpy
import bob.ap
import bob.core

import logging
logger = logging.getLogger("bob.bio.spear")
logger.setLevel(logging.DEBUG)

from bob.bio.base.extractor import Extractor
from .. import utils


class CepstralExtended(Extractor):
    """Extract energy bands from spectrogram and VAD labels based on the modulation of the energy around 4 Hz"""

    def __init__(
            self,
            win_length_ms=20.,  # 20 ms
            win_shift_ms=10.,  # 10 ms
            n_filters=40,
            f_min=0.0,  # 0 Hz
            f_max=8000,  # 8 KHz - this is an important value. Normally it should be half of the sampling frequency
            pre_emphasis_coef=1.0,
            mel_scale=True,
            rect_filter=False,
            inverse_filter=False,
            delta_win=2,
            n_ceps=19,  # 0-->18,
            dct_norm=False,
            ssfc_features=False,
            scfc_features=False,
            scmc_features=False,
            with_delta=True,
            with_delta_delta=True,
            with_energy=False,
            normalize_spectrum=False,
            keep_only_deltas=True,
            log_filter=True,
            energy_filter=False,
            vad_filter="no_filter",  # we do apply any trim filter by default
            normalize_feature_vector = False,
            **kwargs
    ):
        # call base class constructor with its set of parameters
        Extractor.__init__(
            self,
            requires_training=False, split_training_data_by_client=False,
            **kwargs
        )
        # copy parameters
        self.win_length_ms = win_length_ms
        self.win_shift_ms = win_shift_ms
        self.n_filters = n_filters
        self.f_min = f_min
        self.f_max = f_max
        self.pre_emphasis_coef = pre_emphasis_coef
        self.mel_scale = mel_scale
        self.rect_filter = rect_filter
        self.inverse_filter = inverse_filter
        self.delta_win = delta_win
        self.n_ceps = n_ceps
        self.dct_norm = dct_norm
        self.ssfc_features = ssfc_features
        self.scfc_features = scfc_features
        self.scmc_features = scmc_features
        self.with_delta = with_delta
        self.with_delta_delta = with_delta_delta
        self.with_energy = with_energy
        self.normalize_spectrum = normalize_spectrum
        self.keep_only_deltas = keep_only_deltas
        self.log_filter = log_filter
        self.energy_filter = energy_filter
        self.vad_filter = vad_filter
        self.normalize_feature_vector = normalize_feature_vector

        # compute the size of the feature vector
        self.features_len = self.n_ceps
        if self.with_delta:
            self.features_len += self.n_ceps
        if self.with_delta_delta:
            self.features_len += self.n_ceps


    def normalize_features(self, features):
        mean = numpy.mean(features, axis=0)
        std = numpy.std(features, axis=0)
        return numpy.divide(features-mean, std)


    def compute_ceps(self, rate, data):

        ceps = bob.ap.Ceps(rate, self.win_length_ms, self.win_shift_ms, self.n_filters, self.n_ceps, self.f_min,
                           self.f_max, self.delta_win, self.pre_emphasis_coef)
        ceps.dct_norm = self.dct_norm
        ceps.mel_scale = self.mel_scale
        # ceps.mel_scale = False
        ceps.rect_filter = self.rect_filter
        ceps.inverse_filter = self.inverse_filter
        ceps.with_energy = self.with_energy
        ceps.with_delta = self.with_delta
        ceps.with_delta_delta = self.with_delta_delta
        ceps.ssfc_features = self.ssfc_features
        ceps.scfc_features = self.scfc_features
        ceps.scmc_features = self.scmc_features
        ceps.normalize_spectrum = self.normalize_spectrum
        ceps.log_filter = self.log_filter
        ceps.energy_filter = self.energy_filter

        cepstral_features = ceps(data)

        if self.keep_only_deltas: # do not take the actual coefficients, only delta with delta-delta
            cepstral_features = cepstral_features[:, self.n_ceps:]
        return cepstral_features

    def __call__(self, input_data, annotations=None):
        """labels speech (1) and non-speech (0) parts of the given input wave file using 4Hz modulation energy and energy, as well as, compute energy of the signal and split it in bands using on linear or mel-filters
            Input parameter:
               * input_signal[0] --> rate
               * input_signal[1] --> signal
        """
        rate = input_data[0]
        wav_sample = input_data[1]
        labels = input_data[2] # results of the VAD preprocessor

        # remove trailing zeros the wav_sample
        # wav_sample = numpy.trim_zeros(wav_sample)  # comment it out to align with VAD output

        if wav_sample.size:
            cepstral_coeff = self.compute_ceps(rate, wav_sample)

            # SSFC features are a frame shorter than labels,
            # since they are computed using the difference between neighboring frames
            if self.ssfc_features:
                labels = labels[1:]
            logger.info("- Extraction: size of cepstral features %s", str(cepstral_coeff.shape))

            filtered_features = utils.vad_filter_features(labels, cepstral_coeff, self.vad_filter)
            logger.info("- Extraction: size of filtered cepstral features %s", str(filtered_features.shape))

            if numpy.isnan(numpy.sum(filtered_features)):
                logger.error("- Extraction: cepstral coefficients have NaN values, returning zero-vector...")
                return numpy.array([numpy.zeros(self.features_len)])

            if self.normalize_feature_vector:
                filtered_features = self.normalize_features(filtered_features)

            return numpy.asarray(filtered_features, dtype=numpy.float64)

        logger.error("- Extraction: WAV sample is empty")
        return numpy.array([numpy.zeros(self.features_len)])


extractor = CepstralExtended()
