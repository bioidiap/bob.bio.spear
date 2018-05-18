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

import numpy
import bob
import math
from .. import utils
import logging
logger = logging.getLogger("bob.bio.spear")

from .Base import Base
from bob.bio.base.preprocessor import Preprocessor


class Energy_Thr(Base):
  """VAD based on the thresholded energy """
  def __init__(
      self,
      win_length_ms = 20.,        # 20 ms
      win_shift_ms = 10.,           # 10 ms
      smoothing_window = 10, # 10 frames (i.e. 100 ms)
      ratio_threshold = 0.15,       # 0.1 of the maximum energy
      **kwargs
  ):
      # call base class constructor with its set of parameters
    Preprocessor.__init__(
        self,
        win_length_ms = win_length_ms,
        win_shift_ms = win_shift_ms,
        smoothing_window = smoothing_window,
        ratio_threshold = ratio_threshold,
    )
    # copy parameters
    self.win_length_ms = win_length_ms
    self.win_shift_ms = win_shift_ms
    self.smoothing_window = smoothing_window
    self.ratio_threshold = ratio_threshold


  def _voice_activity_detection(self, energy):

    n_samples = len(energy)
    threshold = numpy.max(energy) - numpy.log((1./self.ratio_threshold) * (1./self.ratio_threshold))
    label = numpy.array(numpy.ones(n_samples), dtype=numpy.int16)

    # if energy does not change a lot, it's not audio maybe?
    if numpy.std(energy) < 10e-5:
      return label * 0

    k=0
    for i in range(n_samples):
      if energy[i] > threshold:
        label[i]=label[i] * 1
      else:
        label[i]=0
    return label



  def _compute_energy(self, rate_wavsample):
    """retreive the speech / non speech labels for the speech sample given by the tuple (rate, wave signal)"""

    e = bob.ap.Energy(rate_wavsample[0], self.win_length_ms, self.win_shift_ms)
    energy_array = e(rate_wavsample[1])
    labels = self._voice_activity_detection(energy_array)
    # discard isolated speech a number of frames defined in smoothing_window
    labels = utils.smoothing(labels,self.smoothing_window)
    logger.info("After thresholded Energy-based VAD there are %d frames remaining over %d", numpy.sum(labels), len(labels))
    return labels


  def __call__(self, input_signal, annotations=None):
    """labels speech (1) and non-speech (0) parts of the given input wave file using thresholded Energy
        Input parameter:
           * input_signal[0] --> rate
           * input_signal[1] --> signal
        """

    labels = self._compute_energy(input_signal)
    rate    =  input_signal[0]
    data = input_signal[1]
    if (labels == 0).all():
      logger.warn("No Audio was detected in the sample!")
      return None

    return rate, data, labels
