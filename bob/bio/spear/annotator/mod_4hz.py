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

"""{4Hz modulation energy and energy}-based voice activity detection for speaker recognition"""

import logging

import numpy
import scipy.signal

from bob.bio.base.annotator import Annotator

from .. import audio_processing as ap
from .. import utils

logger = logging.getLogger(__name__)


class Mod_4Hz(Annotator):
    """VAD based on the modulation of the energy around 4 Hz and the energy"""

    def __init__(
        self,
        max_iterations=10,  # 10 iterations for the
        convergence_threshold=0.0005,
        variance_threshold=0.0005,
        win_length_ms=20.0,  # 20 ms
        win_shift_ms=10.0,  # 10 ms
        smoothing_window=10,  # 10 frames (i.e. 100 ms)
        n_filters=40,
        f_min=0.0,  # 0 Hz
        f_max=4000,  # 4 KHz
        pre_emphasis_coef=1.0,
        ratio_threshold=0.1,  # 0.1 of the maximum energy
        **kwargs
    ):
        super().__init__(**kwargs)
        self.max_iterations = max_iterations
        self.convergence_threshold = convergence_threshold
        self.variance_threshold = variance_threshold
        self.win_length_ms = win_length_ms
        self.win_shift_ms = win_shift_ms
        self.smoothing_window = smoothing_window
        self.n_filters = n_filters
        self.f_min = f_min
        self.f_max = f_max
        self.pre_emphasis_coef = pre_emphasis_coef
        self.ratio_threshold = ratio_threshold

    def _voice_activity_detection(self, energy, mod_4hz):

        n_samples = len(energy)
        threshold = numpy.max(energy) - numpy.log(
            (1.0 / self.ratio_threshold) * (1.0 / self.ratio_threshold)
        )
        labels = numpy.array(numpy.zeros(n_samples), dtype=numpy.int16)
        # if energy does not change a lot, it's not audio maybe?
        if numpy.std(energy) < 10e-5:
            return labels * 0

        for i in range(n_samples):
            if energy[i] > threshold and mod_4hz[i] > 0.9:
                labels[i] = 1

        # If speech part less then 10 seconds and less than the half of the segment duration, try to find speech with more risk
        if (
            numpy.sum(labels) < 2000
            and float(numpy.sum(labels)) / float(len(labels)) < 0.5
        ):
            # TRY WITH MORE RISK 1...
            for i in range(n_samples):
                if energy[i] > threshold and mod_4hz[i] > 0.5:
                    labels[i] = 1

        if (
            numpy.sum(labels) < 2000
            and float(numpy.sum(labels)) / float(len(labels)) < 0.5
        ):
            # TRY WITH MORE RISK 2...
            for i in range(n_samples):
                if energy[i] > threshold and mod_4hz[i] > 0.2:
                    labels[i] = 1

        if (
            numpy.sum(labels) < 2000
            and float(numpy.sum(labels)) / float(len(labels)) < 0.5
        ):  # This is special for short segments (less than 2s)...
            # TRY WITH MORE RISK 3...
            if (
                (len(energy) < 200)
                or (numpy.sum(labels) == 0)
                or (numpy.mean(labels) < 0.025)
            ):
                for i in range(n_samples):
                    if energy[i] > threshold:
                        labels[i] = 1
        return labels

    def averaging(self, list_1s_shift):
        len_list = len(list_1s_shift)
        sample_level_value = numpy.array(numpy.zeros(len_list, dtype=float))
        sample_level_value[0] = numpy.array(list_1s_shift[0])
        for j in range(2, numpy.min([len_list, 100])):
            sample_level_value[j - 1] = ((j - 1.0) / j) * sample_level_value[
                j - 2
            ] + (1.0 / j) * numpy.array(list_1s_shift[j - 1])
        for j in range(numpy.min([len_list, 100]), len_list - 100 + 1):
            sample_level_value[j - 1] = numpy.array(
                numpy.mean(list_1s_shift[j - 100 : j])
            )
        sample_level_value[len_list - 1] = list_1s_shift[len_list - 1]
        for j in range(2, numpy.min([len_list, 100]) + 1):
            sample_level_value[len_list - j] = (
                (j - 1.0) / j
            ) * sample_level_value[len_list + 1 - j] + (1.0 / j) * numpy.array(
                list_1s_shift[len_list - j]
            )
        return sample_level_value

    def bandpass_firwin(self, ntaps, lowcut, highcut, fs, window="hamming"):
        nyq = 0.5 * fs
        taps = scipy.signal.firwin(
            ntaps,
            [lowcut, highcut],
            nyq=nyq,
            pass_zero=False,
            window=window,
            scale=True,
        )
        return taps

    def pass_band_filtering(self, energy_bands, fs):
        energy_bands = energy_bands.T
        order = 8
        Wo = 4.0
        num_taps = self.bandpass_firwin(order + 1, (Wo - 0.5), (Wo + 0.5), fs)
        res = scipy.signal.lfilter(num_taps, 1.0, energy_bands)
        return res

    def modulation_4hz(self, filtering_res, data, sample_rate):
        fs = sample_rate
        win_length = int(fs * self.win_length_ms / 1000)
        win_shift = int(fs * self.win_shift_ms / 1000)
        Energy = filtering_res.sum(axis=0)
        mean_Energy = numpy.mean(Energy)
        Energy = Energy / mean_Energy

        # win_size = int(2.0 ** math.ceil(math.log(win_length) / math.log(2)))
        n_frames = 1 + (data.shape[0] - win_length) // win_shift
        range_modulation = int(fs / win_length)  # This corresponds to 1 sec
        res = numpy.zeros(n_frames)
        if n_frames < range_modulation:
            return res
        for w in range(0, n_frames - range_modulation):
            E_range = Energy[
                w : w + range_modulation
            ]  # computes the modulation every 10 ms
            if (E_range <= 0.0).any():
                res[w] = 0
            else:
                res[w] = numpy.var(numpy.log(E_range))
        res[n_frames - range_modulation : n_frames] = res[
            n_frames - range_modulation - 1
        ]
        return res

    def mod_4hz(self, data, sample_rate):
        """Computes and returns the 4Hz modulation energy features for the given input wave file"""

        energy_bands = ap.spectrogram(
            data,
            sample_rate,
            win_length_ms=self.win_length_ms,
            win_shift_ms=self.win_shift_ms,
            n_filters=self.n_filters,
            f_min=self.f_min,
            f_max=self.f_max,
            pre_emphasis_coef=self.pre_emphasis_coef,
            energy_filter=True,
            log_filter=False,
            energy_bands=True,
        )
        filtering_res = self.pass_band_filtering(energy_bands, sample_rate)
        mod_4hz = self.modulation_4hz(filtering_res, data, sample_rate)
        mod_4hz = self.averaging(mod_4hz)
        energy_array = ap.energy(
            data,
            sample_rate,
            win_length_ms=self.win_length_ms,
            win_shift_ms=self.win_shift_ms,
        )
        labels = self._voice_activity_detection(energy_array, mod_4hz)
        labels = utils.smoothing(
            labels, self.smoothing_window
        )  # discard isolated speech less than 100ms
        logger.info(
            "After Mod-4Hz based VAD there are %d frames remaining over %d",
            numpy.sum(labels),
            len(labels),
        )
        return labels, energy_array, mod_4hz

    def transform_one(self, data, sample_rate):
        """labels speech (1) and non-speech (0) parts of the given input wave file using 4Hz modulation energy and energy
        Input parameter:
           * input_signal[0] --> rate
           * input_signal[1] --> signal TODO doc
        """
        [labels, energy_array, mod_4hz] = self.mod_4hz(data, sample_rate)
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
