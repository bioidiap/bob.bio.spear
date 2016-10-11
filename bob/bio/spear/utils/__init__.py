#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Laurent El Shafey <Laurent.El-Shafey@idiap.ch>
# Roy Wallace <roy.wallace@idiap.ch>
# Elie Khoury <Elie.Khoury@idiap.ch>
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

from .extraction import *

import os
import numpy

def ensure_dir(dirname):
  """ Creates the directory dirname if it does not already exist,
      taking into account concurrent 'creation' on the grid.
      An exception is thrown if a file (rather than a directory) already
      exists. """
  try:
    # Tries to create the directory
    os.makedirs(dirname)
  except OSError:
    # Check that the directory exists
    if os.path.isdir(dirname): pass
    else: raise



def convertScoreToList(scores, probes):
  ret = []
  i = 0
  for k in sorted(probes):
    ret.append((probes[k][1], probes[k][2], probes[k][3], probes[k][4], scores[i]))
    i+=1
  return ret


def convertScoreDictToList(scores, probes):
  ret = []
  i = 0
  for k in sorted(probes):
    ret.append((probes[k][1], probes[k][2], probes[k][3], probes[k][4], scores[i]))
    i+=1
  return ret

def convertScoreListToList(scores, probes):
  ret = []
  i = 0
  for p in probes:
    ret.append((p[1], p[2], p[3], p[4], scores[i]))
    i+=1
  return ret

def probes_used_generate_vector(probe_files_full, probe_files_model):
  """Generates boolean matrices indicating which are the probes for each model"""
  import numpy as np
  C_probesUsed = np.ndarray((len(probe_files_full),), 'bool')
  C_probesUsed.fill(False)
  c=0
  for k in sorted(probe_files_full.keys()):
    if probe_files_model.has_key(k): C_probesUsed[c] = True
    c+=1
  return C_probesUsed

def probes_used_extract_scores(full_scores, same_probes):
  """Extracts a matrix of scores for a model, given a probes_used row vector of boolean"""
  if full_scores.shape[1] != same_probes.shape[0]: raise "Size mismatch"
  import numpy as np
  model_scores = np.ndarray((full_scores.shape[0],np.sum(same_probes)), 'float64')
  c=0
  for i in range(0,full_scores.shape[1]):
    if same_probes[i]:
      for j in range(0,full_scores.shape[0]):
        model_scores[j,c] = full_scores[j,i]
      c+=1
  return model_scores


def read(filename):
  """Read audio file"""
  # Depricated: use load() function from bob.bio.spear.database.AudioBioFile
  #TODO: update xbob.sox first. This will enable the use of formats like NIST sphere and other
  #import xbob.sox
  #audio = xbob.sox.reader(filename)
  #(rate, data) = audio.load()
  # We consider there is only 1 channel in the audio file => data[0]
  #data= numpy.cast['float'](data[0]*pow(2,15)) # pow(2,15) is used to get the same native format as for scipy.io.wavfile.read
  import scipy.io.wavfile
  rate, audio = scipy.io.wavfile.read(filename)

  # We consider there is only 1 channel in the audio file => data[0]
  data= numpy.cast['float'](audio)
  return rate, data



def normalize_std_array(vector):
  """Applies a unit mean and variance normalization to an arrayset"""

  # Initializes variables
  length = 1
  n_samples = len(vector)
  mean = numpy.ndarray((length,), 'float64')
  std = numpy.ndarray((length,), 'float64')
  mean.fill(0)
  std.fill(0)

  # Computes mean and variance
  for array in vector:
    x = array.astype('float64')
    mean += x
    std += (x ** 2)

  mean /= n_samples
  std /= n_samples
  std -= (mean ** 2)
  std = std ** 0.5
  arrayset = numpy.ndarray(shape=(n_samples,mean.shape[0]), dtype=numpy.float64)

  for i in range (0, n_samples):
    arrayset[i,:] = (vector[i]-mean) / std
  return arrayset


def smoothing(labels, smoothing_window):
  """ Applies a smoothing on VAD"""

  if numpy.sum(labels)< smoothing_window:
    return labels
  segments = []
  for k in range(1,len(labels)-1):
    if labels[k]==0 and labels[k-1]==1 and labels[k+1]==1 :
      labels[k]=1
  for k in range(1,len(labels)-1):
    if labels[k]==1 and labels[k-1]==0 and labels[k+1]==0 :
      labels[k]=0

  seg = numpy.array([0,0,labels[0]])
  for k in range(1,len(labels)):
    if labels[k] != labels[k-1]:
      seg[1]=k-1
      segments.append(seg)
      seg = numpy.array([k,k,labels[k]])
  seg[1]=len(labels)-1
  segments.append(seg)

  if len(segments) < 2:
    return labels

  curr = segments[0]
  next = segments[1]

  # Look at the first segment. If it's short enough, just change its labels
  if (curr[1]-curr[0]+1) < smoothing_window and (next[1]-next[0]+1) > smoothing_window:
    if curr[2]==1:
      labels[curr[0] : (curr[1]+1)] = numpy.zeros(curr[1] - curr[0] + 1)
      curr[2]=0
    else: #curr[2]==0
      labels[curr[0] : (curr[1]+1)] = numpy.ones(curr[1] - curr[0] + 1)
      curr[2]=1

  for k in range(1,len(segments)-1):
    prev = segments[k-1]
    curr = segments[k]
    next = segments[k+1]

    if (curr[1]-curr[0]+1) < smoothing_window and (prev[1]-prev[0]+1) > smoothing_window and (next[1]-next[0]+1) > smoothing_window:
      if curr[2]==1:
        labels[curr[0] : (curr[1]+1)] = numpy.zeros(curr[1] - curr[0] + 1)
        curr[2]=0
      else: #curr[2]==0
        labels[curr[0] : (curr[1]+1)] = numpy.ones(curr[1] - curr[0] + 1)
        curr[2]=1

  prev = segments[-2]
  curr = segments[-1]

  if (curr[1]-curr[0]+1) < smoothing_window and (prev[1]-prev[0]+1) > smoothing_window:
    if curr[2]==1:
      labels[curr[0] : (curr[1]+1)] = numpy.zeros(curr[1] - curr[0] + 1)
      curr[2]=0
    else: #if curr[2]==0
      labels[curr[0] : (curr[1]+1)] = numpy.ones(curr[1] - curr[0] + 1)
      curr[2]=1

  return labels

# gets sphinx autodoc done right - don't remove it
__all__ = [_ for _ in dir() if not _.startswith('_')]
