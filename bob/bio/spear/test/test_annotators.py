#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# @author: Elie Khoury <Elie.Khoury@idiap.ch>
# @date: Tue  9 Jun 23:10:43 CEST 2015
#
# Copyright (C) 2011-2012 Idiap Research Institute, Martigny, Switzerland
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


import os

import h5py
import numpy as np
import pkg_resources

import bob.bio.base
import bob.bio.spear

regenerate_refs = False


def _compare(
    data, reference, write_function=bob.bio.base.save, read_function=bob.bio.base.load
):
    # write reference?
    if regenerate_refs:
        write_function(data, reference)

    # compare reference
    reference = h5py.File(reference, "r")
    # # 1. check rate
    # np.testing.assert_allclose(data[0], reference[0], atol=1e-5)
    # # 2. check sample data
    # np.testing.assert_allclose(data[1], reference[1], atol=1e-5)
    # 3. check VAD labels
    np.testing.assert_allclose(data, reference["labels"], atol=1e-5)


def _wav(filename="data/sample.wav"):
    path = pkg_resources.resource_filename("bob.bio.spear.test", filename)
    path, ext = os.path.splitext(path)
    directory, path = os.path.split(path)
    base_audiobiofile = bob.bio.spear.database.AudioBioFile(
        "client_id", path, "file_id"
    )
    return base_audiobiofile.load(directory, ext)


# def test_smoothing():
#     for labels in [
#         np.array([0,0,0,0,1,0,1,1,1,1,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,1,1,1,1,0,0,1,1,1,1,1,0,0]),
#         np.array([0,0,0,0,1,0,0,0,0]),
#         np.array([1,1,1,1,0,1,1,1,1]),
#         np.array([0,0,0,0,1,0,0,0,0,1,1,1,1,0,0]),
#         np.array([1,0,0,0,1,0,0,0,0,1,1,1,0,0]),
#         np.array([0,1,1,1,0,1,1,1,1,0,0,0,1]),
#         np.array([0,1,1,1,0,0,0,1,1,1,0,0,0,0,1,1,0,0,0,0,1]),
#     ]:
#         ref = old_smoothing(labels.copy(), 3)
#         smooth = smoothing(da.array(labels), 3).compute()
#         print("l,n,r")
#         for l,s,r in zip(labels,smooth,ref):
#             print(l, s, r)
#         np.testing.assert_array_equal(smooth, ref)


def test_energy_2gauss():
    # read input
    wav = _wav()
    annotator = bob.bio.base.load_resource("energy-2gauss", "annotator")
    assert isinstance(annotator, bob.bio.spear.annotator.Energy_2Gauss)

    # test the energy-based VAD annotator
    annotator = bob.bio.spear.annotator.Energy_2Gauss()
    _compare(
        annotator.transform_one(wav[1], wav[0]),
        pkg_resources.resource_filename(
            "bob.bio.spear.test", "data/vad_energy_2gauss.hdf5"
        ),
    )


# def test_energy_thr():
#     # read input
#     wav = _wav()
#     preprocessor = bob.bio.base.load_resource("energy-thr", "preprocessor")
#     assert isinstance(preprocessor, bob.bio.spear.preprocessor.Energy_Thr)

#     # test the energy-based VAD preprocessor
#     preprocessor = bob.bio.spear.preprocessor.Energy_Thr()
#     _compare(
#         preprocessor(wav),
#         pkg_resources.resource_filename(
#             "bob.bio.spear.test", "data/vad_energy_thr.hdf5"
#         ),
#         preprocessor.write_data,
#         preprocessor.read_data,
#     )


# def test_mod_4hz():
#     # read input
#     wav = _wav()
#     preprocessor = bob.bio.base.load_resource("mod-4hz", "preprocessor")
#     assert isinstance(preprocessor, bob.bio.spear.preprocessor.Mod_4Hz)

#     # test the Mod-4hz based VAD preprocessor
#     preprocessor = bob.bio.spear.preprocessor.Mod_4Hz()
#     _compare(
#         preprocessor(wav),
#         pkg_resources.resource_filename("bob.bio.spear.test", "data/vad_mod_4hz.hdf5"),
#         preprocessor.write_data,
#         preprocessor.read_data,
#     )


# def test_mute_audio():
#     # read input
#     wav = _wav("data/silence.wav")
#     for preprocessor in [
#         bob.bio.spear.preprocessor.Mod_4Hz(),
#         bob.bio.spear.preprocessor.Energy_Thr(),
#         bob.bio.spear.preprocessor.Energy_2Gauss(),
#     ]:
#         # test VAD returns None
#         data = preprocessor(wav)
#         assert data is None, (preprocessor, data)
