#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Elie Khoury <Elie.Khoury@idiap.ch>
# Fri Aug 30 11:43:30 CEST 2013
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


import numpy
import bob
from .. import utils
from bob.bio.base.preprocessor import Preprocessor
from .Base import Base

class External(Base):
  """Uses external VAD and converts it to fit the format used by Spear"""
  def __init__(
      self,
      win_length_ms = 20.,        # 20 ms
      win_shift_ms = 10.,           # 10 ms 
      **kwargs
  ):
      # call base class constructor with its set of parameters
    Preprocessor.__init__(
        self,
        win_length_ms = win_length_ms,
        win_shift_ms = win_shift_ms, 
    )
    # copy parameters
    self.win_length_ms = win_length_ms
    self.win_shift_ms = win_shift_ms
  
  def use_existing_vad(self, inArr, vad_file):
    f=open(vad_file)
    n_samples = len(inArr)
    labels = numpy.array(numpy.zeros(n_samples), dtype=numpy.int16)
    ns=0
    for line in f:
      line = line.strip()
      st_frame = float(line.split(' ')[2])
      en_frame = float(line.split(' ')[4])
      st_frame = min(int(st_frame * 100), n_samples)
      st_frame = max(st_frame, 0)
      en_frame = min(int(en_frame * 100), n_samples)
      en_frame = max(en_frame, 0)
      for i in range(st_frame, en_frame):
        labels[i]=1
    
    return labels


  
  def _conversion(self, input_signal, vad_file):
    """
      Converts an external VAD to follow the Spear convention.
      Energy is used in order to avoind out-of-bound array indexes.
    """
    
    e = bob.ap.Energy(rate_wavsample[0], self.win_length_ms, self.win_shift_ms)
    energy_array = e(rate_wavsample[1])
    labels = self.use_existing_vad(energy_array, vad_file)
    
    return labels
    
  def __call__(self, input_signal, annotations=None):
    """labels speech (1) and non-speech (0) parts using an external VAD segmentation
        Input parameter:
           * input_signal[0] --> rate
           * input_signal[1] --> signal 
           * annotations --> the external VAD annotations
        """
    labels = self._conversion(input_signal, annotations)
    rate    =  input_signal[0]
    data = input_signal[1]
    return rate, data, labels
