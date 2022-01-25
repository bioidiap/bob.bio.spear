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

import dask.array as da
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


def convertScoreToList(scores, probes):  # TODO remove if not used anywhere.
    ret = []
    i = 0
    # YD2021: Why are the probes reordered, but not the scores?
    for k in sorted(probes):
        ret.append((probes[k][1], probes[k][2], probes[k][3], probes[k][4], scores[i]))
        i += 1
    return ret


def convertScoreDictToList(scores, probes):  # TODO remove if not used anywhere.
    ret = []
    i = 0
    # YD2021: Why are the probes reordered, but not the scores?
    for k in sorted(probes):
        ret.append((probes[k][1], probes[k][2], probes[k][3], probes[k][4], scores[i]))
        i += 1
    return ret


def convertScoreListToList(scores, probes):  # TODO remove if not used anywhere.
    return [(p[1], p[2], p[3], p[4], s) for s, p in zip(scores, probes)]


def probes_used_generate_vector(
    probe_files_full, probe_files_model
):  # TODO remove if not used anywhere.
    """Generates boolean matrices indicating which are the probes for each model"""
    C_probesUsed = np.full(shape=(len(probe_files_full),), fill_value=False, dtype=bool)
    for c, k in enumerate(sorted(probe_files_full.keys())):
        if k in probe_files_model:
            C_probesUsed[c] = True
    return C_probesUsed


def probes_used_extract_scores(
    full_scores, same_probes
):  # TODO remove if not used anywhere.
    """Extracts a matrix of scores for a model, given a probes_used row vector of boolean"""
    if full_scores.shape[1] != same_probes.shape[0]:
        raise "Size mismatch"

    model_scores = np.ndarray((full_scores.shape[0], np.sum(same_probes)), "float64")
    c = 0
    for i in range(0, full_scores.shape[1]):
        if same_probes[i]:
            for j in range(0, full_scores.shape[0]):
                model_scores[j, c] = full_scores[j, i]
            c += 1
    return model_scores


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


def new_smoothing(labels, smoothing_window):
    """Applies a smoothing on VAD. 20211115: WIP

    YD: From what I understand reading the old code:
        Swaps the labels if the number of consecutive values is less than the window,
        and the neighbors groups of consecutive values are bigger than the window.
    """
    if labels.sum() < smoothing_window:
        return labels

    # Remove single 0s, then 1s
    labels = np.concatenate(
        (
            labels[0:0],
            np.where(
                np.logical_and(labels == 0, np.roll(labels, 1) == np.roll(labels, -1)),
                np.roll(labels, 1),
                labels,
            ),
            labels[-1:-1],
        )
    )
    labels = np.concatenate(
        (
            labels[0:0],
            np.where(
                np.logical_and(labels == 1, np.roll(labels, 1) == np.roll(labels, -1)),
                np.roll(labels, 1),
                labels,
            ),
            labels[-1:-1],
        )
    )

    # labels = labels.compute()

    # segments = []  # list[list[start_index, end_index, label_value]]
    toggles = np.concatenate(([True], labels[:-1] != labels[1:]))
    segments = (
        np.flatnonzero(toggles).compute_chunk_sizes()
        if isinstance(toggles, da.Array)
        else np.flatnonzero(toggles)
    )

    if segments.shape[0] <= 2:
        return labels

    starting_value = labels[0]

    # segments_stacked = np.vstack((segments, np.roll(segments, 1), np.roll(segments, -1)))

    smoothed_segments = None

    current = 3

    # Look at the first segment. If it's too short, merge it with the second
    if segments[1] - segments[0] < smoothing_window < segments[2] - segments[1]:
        starting_value = (starting_value + 1) % 2
        print("Toggle starting segment. Now", starting_value)
        # current -= 1
    else:
        smoothed_segments = segments[0:0]
        print(f"Adding first segment 1 ({segments[1]})")

    while current < len(segments) - 1:
        print("current =", current)
        if (
            segments[current] - segments[current - 1] < smoothing_window
            and segments[current - 1] - segments[current - 2] > smoothing_window
            and segments[current + 1] - segments[current] > smoothing_window
        ):
            print(f"Toggle segment {current} ({segments[current]})")
            current += 1
        else:
            # if (
            #     segments[current] - segments[current - 1] > smoothing_window
            #     or segments[current - 1] - segments[current - 2] < smoothing_window
            #     or segments[current + 1] - segments[current] < smoothing_window
            # ):
            # if smoothed_segments is None:
            #     smoothed_segments = segments[current-1:current-1]
            # else:
            smoothed_segments = np.concatenate((smoothed_segments, [current - 1]))
            print(f"Adding segment {current-1} ({segments[current-1]})")
        current += 1
    print("out current =", current)

    # Look at the last segment. If it's too short, toggle its labels
    # if segments[-1]-segments[-2] < smoothing_window < segments[-2]-segments[-3]:
    #     print(f"Adding last segment ({segments[-1]})")
    #     smoothed_segments.append(segments[-1])
    # else:
    #     print("Toggle last segment")
    #     smoothed_segments.append(segments[-1])

    if (
        current <= len(segments)
        and segments[-1] - segments[-2]
        < smoothing_window
        <= segments[-2] - segments[-3]
    ):
        print(f"Adding last segment ({segments[-1]})")
        smoothed_segments = np.concatenate((smoothed_segments, segments[-1]))

    print("SMOOTHED:", smoothed_segments.compute())
    labels_count = labels.shape[0]
    labels = []
    prv_segment = 0
    current_value = starting_value
    for cur_segment in smoothed_segments:
        rep = np.repeat(
            current_value.reshape(-1), repeats=int(cur_segment - prv_segment)
        )
        labels = np.concatenate((labels, rep)).astype(int)
        current_value = (current_value + 1) % 2
        prv_segment = cur_segment

    rep = np.repeat(current_value.reshape(-1), repeats=int(labels_count - prv_segment))
    labels = np.concatenate((labels, rep)).astype(int)

    # other_value = (starting_value + 1) % 2
    # if segments.shape % 2 == 0:
    #     labels = np.repeat(np.tile([starting_value,other_value], len(segments)//2), segments)
    # else:
    #     labels = np.repeat(np.tile([starting_value,other_value], len(segments)//2+1)[:-1], segments)

    return labels


# gets sphinx autodoc done right - don't remove it
__all__ = [_ for _ in dir() if not _.startswith("_")]
