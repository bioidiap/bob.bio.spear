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

import h5py
import numpy as np
import pkg_resources

import bob.bio.base
import bob.bio.spear

from bob.bio.base.test.utils import is_library_available
from bob.pipelines import Sample, wrap

regenerate_refs = False


def _compare(
    data,
    reference,
    write_function=bob.bio.base.save,
    read_function=bob.bio.base.load,
):
    # Write reference if needed
    if regenerate_refs:
        ref_f = h5py.File(reference, "w")
        ref_f["array"] = data

    # Compare reference
    reference = np.array(h5py.File(reference, "r")["array"])
    np.testing.assert_allclose(data, reference, atol=1e-5)


def _wav(filename="data/sample.wav"):
    path = pkg_resources.resource_filename("bob.bio.spear.test", filename)
    waveform, sample_rate = bob.bio.spear.audio_processing.read(path)
    return sample_rate, waveform


@is_library_available("torchaudio")
def test_energy_2gauss():
    """Loading and running the energy-2gauss annotator."""
    # Test setup and config
    annotator = bob.bio.base.load_resource("energy-2gauss", "annotator")
    assert isinstance(annotator, bob.bio.spear.annotator.Energy_2Gauss)

    # Read input
    rate, wav = _wav()

    # Test the energy-based VAD annotator
    annotator = bob.bio.spear.annotator.Energy_2Gauss()
    _compare(
        annotator.transform_one(wav, sample_rate=rate),
        pkg_resources.resource_filename(
            "bob.bio.spear.test", "data/vad_energy_2gauss.hdf5"
        ),
    )

    # Test the processing of Sample objects and tags of annotator transformer
    wrapped_annotator = wrap(["sample"], annotator)
    samples = [Sample(data=wav, rate=rate)]
    # Attribute `rate` should be passed as `sample_rate` argument of transform (tags)
    result = wrapped_annotator.transform(samples)
    # Annotations should be in attribute `annotations` of result samples (tags)
    _compare(
        result[0].annotations,
        pkg_resources.resource_filename(
            "bob.bio.spear.test", "data/vad_energy_2gauss.hdf5"
        ),
    )


@is_library_available("torchaudio")
def test_mod_4hz():
    """Loading and running the mod-4hz annotator."""
    # Test setup and config
    annotator = bob.bio.base.load_resource("mod-4hz", "annotator")
    assert isinstance(annotator, bob.bio.spear.annotator.Mod_4Hz)

    # Read input
    rate, wav = _wav()

    # Test the VAD annotator
    annotator = bob.bio.spear.annotator.Mod_4Hz()
    _compare(
        annotator.transform_one(wav, sample_rate=rate),
        pkg_resources.resource_filename(
            "bob.bio.spear.test", "data/vad_mod_4hz.hdf5"
        ),
    )

    # Test the processing of Sample objects and tags of annotator transformer
    wrapped_annotator = wrap(["sample"], annotator)
    samples = [Sample(data=wav, rate=rate)]
    # Attribute `rate` should be passed as `sample_rate` argument of transform (tags)
    result = wrapped_annotator.transform(samples)
    # Annotations should be in attribute `annotations` of result samples (tags)
    _compare(
        result[0].annotations,
        pkg_resources.resource_filename(
            "bob.bio.spear.test", "data/vad_mod_4hz.hdf5"
        ),
    )


@is_library_available("torchaudio")
def test_energy_thr():
    """Loading and running the mod-4hz annotator."""
    # Test setup and config
    annotator = bob.bio.base.load_resource("energy-thr", "annotator")
    assert isinstance(annotator, bob.bio.spear.annotator.Energy_Thr)

    # Read input
    rate, wav = _wav()

    # Test the VAD annotator
    annotator = bob.bio.spear.annotator.Energy_Thr()
    _compare(
        annotator.transform_one(wav, sample_rate=rate),
        pkg_resources.resource_filename(
            "bob.bio.spear.test", "data/vad_energy_thr.hdf5"
        ),
    )

    # Test the processing of Sample objects and tags of annotator transformer
    wrapped_annotator = wrap(["sample"], annotator)
    samples = [Sample(data=wav, rate=rate)]
    # Attribute `rate` should be passed as `sample_rate` argument of transform (tags)
    result = wrapped_annotator.transform(samples)
    # Annotations should be in attribute `annotations` of result samples (tags)
    _compare(
        result[0].annotations,
        pkg_resources.resource_filename(
            "bob.bio.spear.test", "data/vad_energy_thr.hdf5"
        ),
    )


@is_library_available("torchaudio")
def test_mute_audio():
    """Running annotators on silence data to ensure None is returned."""
    # read input
    rate, wav = _wav("data/silence.wav")
    for annotator in [
        bob.bio.spear.annotator.Mod_4Hz(),
        bob.bio.spear.annotator.Energy_Thr(),
        bob.bio.spear.annotator.Energy_2Gauss(),
    ]:
        # test VAD returns None
        data = annotator.transform_one(wav, rate)
        assert data is None, (annotator, data)
