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

import os

import numpy as np

from .extraction import calc_mean  # noqa: F401
from .extraction import calc_mean_std  # noqa: F401
from .extraction import calc_std  # noqa: F401
from .extraction import vad_filter_features  # noqa: F401
from .extraction import zeromean_unitvar_norm  # noqa: F401


def ensure_dir(dirname):
    """Creates the directory dirname if it does not already exist,
    taking into account concurrent 'creation' on the grid.
    An exception is thrown if a file (rather than a directory) already
    exists."""
    try:
        # Tries to create the directory
        os.makedirs(dirname)
    except OSError:
        # Check that the directory exists
        if os.path.isdir(dirname):
            pass
        else:
            raise


def read(filename):  # TODO remove
    """Deprecated. Read audio file"""
    # Deprecated: use load() function from bob.bio.spear.database.AudioBioFile
    # TODO: update xbob.sox first. This will enable the use of formats like NIST sphere and other
    # import xbob.sox
    # audio = xbob.sox.reader(filename)
    # (rate, data) = audio.load()
    # We consider there is only 1 channel in the audio file => data[0]
    # data= np.cast['float'](data[0]*pow(2,15)) # pow(2,15) is used to get the same native format as for scipy.io.wavfile.read
    DeprecationWarning("Do not.")
    import scipy.io.wavfile

    rate, audio = scipy.io.wavfile.read(filename)

    # We consider there is only 1 channel in the audio file => data[0]
    data = np.cast["float"](audio)
    return rate, data


def normalize_std_array(vector: np.ndarray):
    """Applies a unit mean and variance normalization to an arrayset"""
    return (
        vector
        if vector.std(axis=0) == 0
        else (vector - vector.mean(axis=0)) / vector.std(axis=0)
    )


def smoothing(labels, smoothing_window):
    """Applies a smoothing on VAD"""

    if np.sum(labels) < smoothing_window:
        return labels

    segments = []
    for k in range(1, len(labels) - 1):
        if labels[k] == 0 and labels[k - 1] == 1 and labels[k + 1] == 1:
            labels[k] = 1
    for k in range(1, len(labels) - 1):
        if labels[k] == 1 and labels[k - 1] == 0 and labels[k + 1] == 0:
            labels[k] = 0

    seg = np.array([0, 0, labels[0]])
    for k in range(1, len(labels)):
        if labels[k] != labels[k - 1]:
            seg[1] = k - 1
            segments.append(seg)
            seg = np.array([k, k, labels[k]])
    seg[1] = len(labels) - 1
    segments.append(seg)

    if len(segments) < 2:
        return labels

    curr = segments[0]
    next = segments[1]

    # Look at the first segment. If it's short enough, just change its labels
    if (curr[1] - curr[0] + 1) < smoothing_window and (
        next[1] - next[0] + 1
    ) > smoothing_window:
        if curr[2] == 1:
            labels[curr[0] : (curr[1] + 1)] = 0
            curr[2] = 0
        else:  # curr[2]==0
            labels[curr[0] : (curr[1] + 1)] = 1
            curr[2] = 1

    for k in range(1, len(segments) - 1):
        prev = segments[k - 1]
        curr = segments[k]
        next = segments[k + 1]

        if (
            (curr[1] - curr[0] + 1) < smoothing_window
            and (prev[1] - prev[0] + 1) > smoothing_window
            and (next[1] - next[0] + 1) > smoothing_window
        ):
            if curr[2] == 1:
                labels[curr[0] : (curr[1] + 1)] = 0
                curr[2] = 0
            else:  # curr[2]==0
                labels[curr[0] : (curr[1] + 1)] = 1
                curr[2] = 1

    prev = segments[-2]
    curr = segments[-1]

    if (curr[1] - curr[0] + 1) < smoothing_window and (
        prev[1] - prev[0] + 1
    ) > smoothing_window:
        if curr[2] == 1:
            labels[curr[0] : (curr[1] + 1)] = 0
            curr[2] = 0
        else:  # if curr[2]==0
            labels[curr[0] : (curr[1] + 1)] = 1
            curr[2] = 1

    return labels


# gets sphinx autodoc done right - don't remove it
__all__ = [_ for _ in dir() if not _.startswith("_")]
