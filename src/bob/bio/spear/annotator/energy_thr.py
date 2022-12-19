#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Elie Khoury <Elie.Khoury@idiap.ch>
# Tue  9 Jun 16:56:01 CEST 2015
#
# Copyright (C) 2012-2015 Idiap Research Institute, Martigny, Switzerland
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

"""Energy-based voice activity detection for speaker recognition"""

import logging

import numpy

from bob.bio.base.annotator import Annotator

from .. import audio_processing as ap
from .. import utils

logger = logging.getLogger(__name__)


class Energy_Thr(Annotator):
    """VAD based on an energy threshold"""

    def __init__(
        self,
        win_length_ms=20.0,  # 20 ms
        win_shift_ms=10.0,  # 10 ms
        smoothing_window=10,  # 10 frames (i.e. 100 ms)
        ratio_threshold=0.15,  # 0.1 of the maximum energy
        **kwargs
    ):
        super().__init__(**kwargs)
        self.win_length_ms = win_length_ms
        self.win_shift_ms = win_shift_ms
        self.smoothing_window = smoothing_window
        self.ratio_threshold = ratio_threshold

    def _voice_activity_detection(self, energy):

        n_samples = len(energy)
        threshold = numpy.max(energy) - numpy.log(
            (1.0 / self.ratio_threshold) * (1.0 / self.ratio_threshold)
        )
        label = numpy.array(numpy.ones(n_samples), dtype=numpy.int16)

        # if energy does not change a lot, it's not audio maybe?
        if numpy.std(energy) < 10e-5:
            return label * 0

        for i in range(n_samples):
            if energy[i] > threshold:
                label[i] = label[i] * 1
            else:
                label[i] = 0
        return label

    def _compute_energy(self, data, sample_rate):
        """retrieve the speech / non speech labels for the speech sample given by the tuple (rate, wave signal)"""

        energy_array = ap.energy(
            data,
            sample_rate,
            win_length_ms=self.win_length_ms,
            win_shift_ms=self.win_shift_ms,
        )
        labels = self._voice_activity_detection(energy_array)
        # discard isolated speech a number of frames defined in smoothing_window
        labels = utils.smoothing(labels, self.smoothing_window)
        logger.info(
            "After thresholded Energy-based VAD there are %d frames remaining over %d",
            numpy.sum(labels),
            len(labels),
        )
        return labels

    def transform_one(self, data, sample_rate, annotations=None):
        """labels speech (1) and non-speech (0) parts of the given input wave file using thresholded Energy
        Input parameter:
           * input_signal[0] --> rate
           * input_signal[1] --> signal TODO doc
        """

        labels = self._compute_energy(data, sample_rate)
        if (labels == 0).all():
            logger.warning("No Audio was detected in the sample!")
            return None

        return labels

    def transform(
        self, audio_signals: "list[numpy.ndarray]", sample_rates: "list[int]"
    ):
        results = []
        for audio_signal, sample_rate in zip(audio_signals, sample_rates):
            results.append(self.transform_one(audio_signal, sample_rate))
        return results

    def _more_tags(self):
        return {
            "requires_fit": False,
            "bob_transform_extra_input": (("sample_rates", "rate"),),
            "bob_output": "annotations",
        }
