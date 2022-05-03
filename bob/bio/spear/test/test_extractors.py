#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# @author: Elie Khoury <Elie.Khoury@idiap.ch>
# @date: Tue  9 Jun 23:10:43 CEST 2015
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


import numpy

import bob.bio.base
import bob.bio.spear

# from .test_annotators import _wav

# import pkg_resources


regenerate_refs = False


def _compare(
    data,
    reference,
    write_function=bob.bio.base.save,
    read_function=bob.bio.base.load,
):
    # write reference?
    if regenerate_refs:
        write_function(data, reference)

    # compare reference
    reference = read_function(reference)
    assert numpy.allclose(data, reference, atol=1e-5)


"""
def test_mfcc():
    # read input wave file
    rate, wav = _wav()

    extractor = bob.bio.base.load_resource("mfcc60", "extractor")
    assert isinstance(extractor, bob.bio.spear.extractor.Cepstral)

    # test the Cepstral extractor
    extractor = bob.bio.spear.extractor.Cepstral()
    # but we need to apply VAD first
    annotator = bob.bio.spear.annotator.Energy_2Gauss()
    annotations = annotator.transform_one(wav, rate)
    _compare(
        extractor.transform_one(wav, rate, annotations),
        pkg_resources.resource_filename(
            "bob.bio.spear.test", "data/mfcc_60.hdf5"
        ),
        bob.bio.base.save,
        bob.bio.base.load,
    )
"""

# def test_lfcc():
#     # read input wave file
#     wav = _wav()

#     extractor = bob.bio.base.load_resource("lfcc-60", "extractor")
#     assert isinstance(extractor, bob.bio.spear.extractor.Cepstral)

#     # test the Cepstral extractor
#     extractor = bob.bio.spear.extractor.Cepstral(mel_scale=False)
#     # but we need to apply VAD first
#     preprocessor = bob.bio.spear.preprocessor.Energy_2Gauss()
#     preprocessed_data = preprocessor(wav)
#     _compare(
#         extractor(preprocessed_data),
#         pkg_resources.resource_filename("bob.bio.spear.test", "data/lfcc_60.hdf5"),
#         extractor.write_feature,
#         extractor.read_feature,
#     )
