#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Milos Cernak <Milos.Cernak@idiap.ch>
# December 2016
#
# Copyright (C) 2012-2016 Idiap Research Institute, Martigny, Switzerland
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

"""Kaldi MFCC Features for speaker recognition"""

import numpy
# import bob.ap
import bob.kaldi
from .. import utils

import logging
logger = logging.getLogger("bob.bio.spear")

from bob.bio.base.extractor import Extractor


class Kaldi(Extractor):
  """ Extracts the Cepstral Kaldi MFCC features """
  def __init__(
      self,
      preemphasis_coefficient = 0.97,
      raw_energy=True,
      frame_length=25,
      frame_shift=10,
      num_ceps=13,
      num_mel_bins=23,
      cepstral_lifter=22,
      low_freq=20,
      high_freq=0,
      dither=1.0,
      snip_edges=True,
      features_mask = numpy.arange(0,39),
      # Normalization
      normalize_flag = False,
      **kwargs
  ):
      # call base class constructor with its set of parameters
    Extractor.__init__(
      self,
      preemphasis_coefficient = preemphasis_coefficient,
      raw_energy = raw_energy,
      frame_length = frame_length,
      frame_shift = frame_shift,
      num_ceps = num_ceps,
      num_mel_bins = num_mel_bins,
      cepstral_lifter = cepstral_lifter,
      low_freq = low_freq,
      high_freq = high_freq,
      dither = dither,
      snip_edges = snip_edges,
      features_mask = features_mask,
      normalize_flag = normalize_flag,
    )
    # copy parameters
    self.preemphasis_coefficient = preemphasis_coefficient
    self.raw_energy = raw_energy
    self.frame_length = frame_length
    self.frame_shift = frame_shift
    self.num_ceps = num_ceps
    self.num_mel_bins = num_mel_bins
    self.cepstral_lifter = cepstral_lifter
    self.low_freq = low_freq
    self.high_freq = high_freq
    self.dither = dither
    self.snip_edges = snip_edges
    self.features_mask = features_mask
    self.normalize_flag = normalize_flag



  def normalize_features(self, params):
  #########################
  ## Initialisation part ##
  #########################

    normalized_vector = [ [ 0 for i in range(params.shape[1]) ] for j in range(params.shape[0]) ]
    for index in range(params.shape[1]):
      vector = numpy.array([row[index] for row in params])
      n_samples = len(vector)
      norm_vector = utils.normalize_std_array(vector)

      for i in range(n_samples):
        normalized_vector[i][index]=numpy.asscalar(norm_vector[i])
    data = numpy.array(normalized_vector)
    return data




  def __call__(self, input_data):
    """Computes and returns normalized cepstral features for the given input data
    input_data[0] --> sampling rate
    input_data[1] -->  sample data
    input_data[2] --> VAD array (either 0 or 1)
    """

    rate       = input_data[0]
    wavsample  = input_data[1]
    vad_labels = input_data[2]

    # Set parameters
    pree = self.preemphasis_coefficient
    en = self.raw_energy
    fl = self.frame_length
    fs = self.frame_shift
    nc = self.num_ceps
    nb = self.num_mel_bins
    cl = self.cepstral_lifter
    lq = self.low_freq
    hf = self.high_freq
    dith = self.dither
    se = self.snip_edges
    
    # import ipdb ; ipdb.set_trace()
    cepstral_features = bob.kaldi.mfcc(wavsample, rate, pree, en, fl, fs, nc, nb, cl, lq, hf, dith, se)

    aligned=numpy.minimum(vad_labels.shape[0],cepstral_features.shape[0])
    cepstral_features=cepstral_features[:aligned]
    vad_labels=vad_labels[:aligned]
    
    features_mask = self.features_mask
    if vad_labels is not None: # don't apply VAD
      filtered_features = numpy.ndarray(shape=((vad_labels == 1).sum(),len(features_mask)), dtype=numpy.float64)
      i=0
      cur_i=0
      for row in cepstral_features:
        if i < len(vad_labels):
          if vad_labels[i]==1:
            for k in range(len(features_mask)):
              filtered_features[cur_i,k] = row[features_mask[k]]
            cur_i = cur_i + 1
          i = i+1
        else:
          if vad_labels[-1]==1:
            if cur_i == cepstral_features.shape[0]:
              for k in range(len(features_mask)):
                filtered_features[cur_i,k] = row[features_mask[k]]
              cur_i = cur_i + 1
          i = i+1
    else:
      filtered_features = cepstral_features

    if self.normalize_flag:
      normalized_features = self.normalize_features(filtered_features)
    else:
      normalized_features = filtered_features
    if normalized_features.shape[0] == 0:
      logger.warn("No speech found for this utterance")
      # But do not keep it empty!!! This avoids errors in next steps
      normalized_features=numpy.array([numpy.zeros(len(features_mask))])
    return normalized_features
