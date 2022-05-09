#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# @author: Elie Khoury <Elie.Khoury@idiap.ch>
# @date: Sun  7 Jun 15:41:03 CEST 2015
#
# Copyright (C) 2012-2015 Idiap Research Institute, Martigny, Switzerland
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

"""Energy-based voice activity detection for speaker recognition"""

import logging

import dask
import numpy as np

from bob.bio.base.annotator import Annotator
from bob.learn.em import GMMMachine, KMeansMachine

from .. import audio_processing as ap
from .. import utils

logger = logging.getLogger(__name__)


class Energy_2Gauss(Annotator):
    """Detects the Voice Activity using the Energy of the signal and 2 Gaussian GMM."""

    def __init__(
        self,
        max_iterations=10,  # 10 iterations for the GMM trainer
        convergence_threshold=0.0005,
        variance_threshold=0.0005,
        win_length_ms=20.0,  # 20 ms
        win_shift_ms=10.0,  # 10 ms
        smoothing_window=10,  # 10 frames (i.e. 100 ms)
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.max_iterations = max_iterations
        self.convergence_threshold = convergence_threshold
        self.variance_threshold = variance_threshold
        self.win_length_ms = win_length_ms
        self.win_shift_ms = win_shift_ms
        self.smoothing_window = smoothing_window

    def _voice_activity_detection(self, energy_array: np.ndarray) -> np.ndarray:
        """Fits a 2 Gaussian GMM on the energy that splits between voice and silence."""
        n_samples = len(energy_array)
        # if energy does not change a lot, it may not be audio?
        if np.std(energy_array) < 10e-5:
            return np.zeros(shape=n_samples)

        # Add an epsilon small Gaussian noise to avoid numerical issues (mainly due to artificial silence).
        energy_array = (1e-6 * np.random.randn(n_samples)) + energy_array

        # Normalize the energy array, make it an array of 1D samples
        normalized_energy = utils.normalize_std_array(energy_array).reshape(
            (-1, 1)
        )

        # Note: self.max_iterations and self.convergence_threshold are used for both
        # k-means and GMM training.
        kmeans_trainer = KMeansMachine(
            n_clusters=2,
            convergence_threshold=self.convergence_threshold,
            max_iter=self.max_iterations,
            init_max_iter=self.max_iterations,
        )
        ubm_gmm = GMMMachine(
            n_gaussians=2,
            trainer="ml",
            update_means=True,
            update_variances=True,
            update_weights=True,
            convergence_threshold=self.convergence_threshold,
            max_fitting_steps=self.max_iterations,
            k_means_trainer=kmeans_trainer,
        )
        ubm_gmm.variance_thresholds = self.variance_threshold

        ubm_gmm.fit(normalized_energy)

        if np.isnan(ubm_gmm.means).any():
            logger.warn("Annotation aborted: File contains NaN's")
            return np.zeros(shape=n_samples, dtype=int)

        # Classify

        # Different behavior dep on which mean represents high energy (higher value)
        labels = ubm_gmm.log_weighted_likelihood(normalized_energy)
        if ubm_gmm.means.argmax() == 0:  # High energy in means[0]
            labels = labels.argmin(axis=0)
        else:  # High energy in means[1]
            labels = labels.argmax(axis=0)

        return labels

    def _compute_energy(
        self, audio_signal: np.ndarray, sample_rate: int
    ) -> np.ndarray:
        """Retrieves the speech / non speech labels for the speech sample in ``audio_signal``"""

        energy_array = ap.energy(
            audio_signal,
            sample_rate,
            win_length_ms=self.win_length_ms,
            win_shift_ms=self.win_shift_ms,
        )
        labels = self._voice_activity_detection(energy_array)

        # discard isolated speech a number of frames defined in smoothing_window
        labels = utils.smoothing(labels, self.smoothing_window)
        logger.debug(
            "After 2 Gaussian Energy-based VAD there are %d frames remaining over %d",
            np.sum(labels),
            len(labels),
        )
        return labels

    def transform_one(self, audio_signal: np.ndarray, sample_rate: int) -> list:
        """labels speech (1) and non-speech (0) parts of the given input wave file using 2 Gaussian-modeled Energy
        Parameters
        ----------
           audio_signal: array
                Audio signal to annotate
           sample_rate: int
               The sample rate in Hertz
        """
        labels = self._compute_energy(
            audio_signal=audio_signal, sample_rate=sample_rate
        )
        if (labels == 0).all():
            logger.warning(
                "Could not annotate: No audio was detected in the sample!"
            )
            return None
        return labels.tolist()

    def transform(
        self, audio_signals: "list[np.ndarray]", sample_rates: "list[int]"
    ):
        with dask.config.set(scheduler="threads"):
            results = []
            for audio_signal, sample_rate in zip(audio_signals, sample_rates):
                results.append(self.transform_one(audio_signal, sample_rate))
            return results

    def fit(self, X, y=None, **fit_params):
        return self

    def _more_tags(self):
        return {
            "requires_fit": False,
            "bob_transform_extra_input": (("sample_rates", "rate"),),
            "bob_output": "annotations",
        }
