#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Pavel Korshunov <Pavel.Korshunov@idiap.ch>
# Tue  22 Sep 17:21:35 CEST 2015
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


import numpy
import logging

logger = logging.getLogger("bob.bio.spear")


def zeromean_unitvar_norm(data, mean, std):
    """ Normalized the data with zero mean and unit variance. Mean and variance are in numpy.ndarray format"""
    return numpy.divide(data - mean, std)


def calc_mean(c0, c1=[]):
    """ Calculates the mean of the data."""
    if c1 != []:
        return (numpy.mean(c0, 0) + numpy.mean(c1, 0)) / 2.
    else:
        return numpy.mean(c0, 0)


def calc_std(c0, c1=[]):
    """ Calculates the variance of the data."""
    if c1 == []:
        return numpy.std(c0, 0)
    prop = float(len(c0)) / float(len(c1))
    if prop < 1:
        p0 = int(math.ceil(1 / prop))
        p1 = 1
    else:
        p0 = 1
        p1 = int(math.ceil(prop))
    return numpy.std(numpy.vstack(p0 * [c0] + p1 * [c1]), 0)


"""
@param c0
@param c1
@param nonStdZero if the std was zero, convert to one. This will avoid a zero division
"""
def calc_mean_std(c0, c1=[], nonStdZero=False):
    """ Calculates both the mean of the data. """
    mi = calc_mean(c0, c1)
    std = calc_std(c0, c1)
    if (nonStdZero):
        std[std == 0] = 1

    return mi, std


def vad_filter_features(vad_labels, features, filter_frames="trim_silence"):
    """ Trim the spectrogram to remove silent head/tails from the speech sample.
    Keep all remaining frames or either speech or non-speech only
    @param: filter_frames: the value is either 'silence_only' (keep the speech, remove everything else),
    'speech_only' (only keep the silent parts), 'trim_silence' (trim silent heads and tails),
    or 'no_filter' (no filter is applied)
     """

    if not features.size:
        raise ValueError("vad_filter_features(): data sample is empty, no features extraction is possible")

    vad_labels = numpy.asarray(vad_labels, dtype=numpy.int8)
    features = numpy.asarray(features, dtype=numpy.float64)
    features = numpy.reshape(features, (vad_labels.shape[0], -1))

    #    logger.info("RatioVectorExtractor, vad_labels shape: %s", str(vad_labels.shape))
    #    print ("RatioVectorExtractor, features max: %f and min: %f" %(numpy.max(features), numpy.min(features)))

    # first, take the whole thing, in case there are problems later
    filtered_features = features

    # if VAD detection worked on this sample
    if vad_labels is not None and filter_frames != "no_filter":
        # make sure the size of VAD labels and sectrogram lenght match
        if len(vad_labels) == len(features):

            # take only speech frames, as in VAD speech frames are 1 and silence are 0
            speech, = numpy.nonzero(vad_labels)
            silences = None
            if filter_frames == "silence_only":
                # take only silent frames - those for which VAD gave zeros
                silences, = numpy.nonzero(vad_labels == 0)

            if len(speech):
                nzstart = speech[0]  # index of the first non-zero
                nzend = speech[-1]  # index of the last non-zero

                if filter_frames == "silence_only":  # extract only silent frames
                    # take only silent frames in-between the speech
                    silences = silences[silences > nzstart]
                    silences = silences[silences < nzend]
                    filtered_features = features[silences, :]
                elif filter_frames == "speech_only":
                    filtered_features = features[speech, :]
                else:  # when we take all
                    filtered_features = features[nzstart:nzend + 1, :]  # numpy slicing is a non-closed interval [)
        else:
            logger.error("vad_filter_features(): VAD labels should be the same length as energy bands")

        logger.info("vad_filter_features(): filtered_features shape: %s", str(filtered_features.shape))

    return filtered_features
