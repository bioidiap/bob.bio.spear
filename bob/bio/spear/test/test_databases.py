#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# @author: Manuel Guenther <Manuel.Guenther@idiap.ch>
# @author: Pavel Korshunov <pavel.korshunov@idiap.ch>
# @date: Thu May 24 10:41:42 CEST 2012
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


from bob.bio.base.database import CSVDataset
from bob.bio.spear.database import SpearBioDatabase
from bob.pipelines import DelayedSample, SampleSet


def _check_database(
    database,
    n_train=None,
    n_dev_references=None,
    n_dev_references_samples=None,
    n_dev_probes=None,
    n_dev_probes_samples=None,
    n_eval_references=None,
    n_eval_references_samples=None,
    n_eval_probes=None,
    n_eval_probes_samples=None,
):
    """Verifies that a SpearBioDatabase instance is constructed correctly.

    Checks the number of samples of each subsets, if a count is provided.
    """

    assert isinstance(database, CSVDataset)

    if n_train:
        train = database.background_model_samples()
        assert len(train) == n_train, f"Wrong train len: {len(train)}"

    if n_dev_references or n_dev_references_samples:
        dev_ref = database.references(group="dev")
        if n_dev_references:
            assert (
                len(dev_ref) == n_dev_references
            ), f"Wrong dev ref len: {len(dev_ref)}"
        assert all(isinstance(s, SampleSet) for s in dev_ref)
        if n_dev_references_samples:
            assert all(
                len(s) == n_dev_references_samples for s in dev_ref
            ), f"Not all dev references haves the same sample count ({len(dev_ref[0])})"
        assert all(isinstance(s, DelayedSample) for s in dev_ref[0])

    if n_dev_probes or n_dev_probes_samples:
        dev_pro = database.probes(group="dev")
        if n_dev_probes:
            assert (
                len(dev_pro) == n_dev_probes
            ), f"Wrong dev probes len: {len(dev_pro)}"
        assert all(isinstance(s, SampleSet) for s in dev_pro)
        if n_dev_probes_samples:
            assert all(
                len(s) == n_dev_probes_samples for s in dev_pro
            ), f"Not all dev probes haves the same sample count ({len(dev_pro[0])})"
        assert all(isinstance(s[0], DelayedSample) for s in dev_pro)

    if n_eval_references or n_eval_references_samples:
        eval_ref = database.references(group="eval")
        if n_eval_references:
            assert (
                len(eval_ref) == n_eval_references
            ), f"Wrong eval ref len: {len(eval_ref)}"
        assert all(isinstance(s, SampleSet) for s in eval_ref)
        if n_eval_references_samples:
            assert all(
                len(s) == n_eval_references_samples for s in eval_ref
            ), f"Not all eval references haves the same sample count ({len(eval_ref[0])})"
        assert all(isinstance(s, DelayedSample) for s in eval_ref[0])

    if n_eval_probes or n_eval_probes_samples:
        eval_pro = database.probes(group="eval")
        if n_eval_probes:
            assert (
                len(eval_pro) == n_eval_probes
            ), f"Wrong eval probes len: {len(eval_pro)}"
        assert all(isinstance(s, SampleSet) for s in eval_pro)
        if n_dev_probes_samples:
            assert all(
                len(s) == n_eval_probes_samples for s in eval_pro
            ), f"Not all eval probes haves the same sample count ({len(eval_pro[0])})"
        assert all(isinstance(s[0], DelayedSample) for s in eval_pro)


def test_mobio_male():
    database = SpearBioDatabase("mobio", protocol="male", data_path="dummy/")

    _check_database(
        database,
        n_train=7104,
        n_dev_references=24,
        n_dev_references_samples=5,
        n_dev_probes=2520,
        n_dev_probes_samples=1,
        n_eval_references=38,
        n_eval_references_samples=5,
        n_eval_probes=3990,
        n_eval_probes_samples=1,
    )


def test_mobio_female():
    database = SpearBioDatabase("mobio", protocol="female", data_path="dummy/")

    _check_database(
        database,
        n_train=2496,
        n_dev_references=18,
        n_dev_references_samples=5,
        n_dev_probes=1890,
        n_dev_probes_samples=1,
        n_eval_references=20,
        n_eval_references_samples=5,
        n_eval_probes=2100,
        n_eval_probes_samples=1,
    )


def test_avspoof_licit():
    database = SpearBioDatabase("avspoof", protocol="licit", data_path="dummy/")

    _check_database(
        database,
        n_train=4973,
        n_dev_references=14,
        n_dev_references_samples=None,  # Variable sample count
        n_dev_probes=4225,
        n_dev_probes_samples=1,
        n_eval_references=16,
        n_eval_references_samples=None,  # Variable sample count
        n_eval_probes=4708,
        n_eval_probes_samples=1,
    )


def test_avspoof_spoof():
    database = SpearBioDatabase("avspoof", protocol="spoof", data_path="dummy/")

    _check_database(
        database,
        n_train=56470,
        n_dev_references=14,
        n_dev_references_samples=None,  # Variable sample count
        n_dev_probes=56470,
        n_dev_probes_samples=1,
        n_eval_references=16,
        n_eval_references_samples=None,  # Variable sample count
        n_eval_probes=63380,
        n_eval_probes_samples=1,
    )


def test_asvspoof_licit():
    database = SpearBioDatabase(
        "asvspoof", protocol="licit", data_path="dummy/"
    )

    _check_database(
        database,
        n_train=None,
        n_dev_references=20,
        n_dev_references_samples=5,
        n_dev_probes=5700,
        n_dev_probes_samples=1,
        n_eval_references=26,
        n_eval_references_samples=5,
        n_eval_probes=10400,
        n_eval_probes_samples=1,
    )


def test_asvspoof_spoof():
    database = SpearBioDatabase(
        "asvspoof", protocol="spoof", data_path="dummy/"
    )

    _check_database(
        database,
        n_train=None,
        n_dev_references=20,
        n_dev_references_samples=5,
        n_dev_probes=28500,
        n_dev_probes_samples=1,
        n_eval_references=26,
        n_eval_references_samples=5,
        n_eval_probes=104000,
        n_eval_probes_samples=1,
    )


def test_voicepa_licit():
    database = SpearBioDatabase(
        "voicepa", protocol="grandtest-licit", data_path="dummy/"
    )

    _check_database(
        database,
        n_train=4973,
        n_dev_references=14,
        n_dev_references_samples=None,  # Variable sample count
        n_dev_probes=4225,
        n_dev_probes_samples=1,
        n_eval_references=16,
        n_eval_references_samples=None,  # Variable sample count
        n_eval_probes=4708,
        n_eval_probes_samples=1,
    )


def test_voicepa_spoof():
    database = SpearBioDatabase(
        "voicepa", protocol="grandtest-spoof", data_path="dummy/"
    )

    _check_database(
        database,
        n_train=115730,
        n_dev_references=14,
        n_dev_references_samples=None,  # Variable sample count
        n_dev_probes=115740,
        n_dev_probes_samples=1,
        n_eval_references=16,
        n_eval_references_samples=None,  # Variable sample count
        n_eval_probes=129988,
        n_eval_probes_samples=1,
    )


def test_timit():
    database = SpearBioDatabase("timit", protocol="2", data_path="dummy/")

    _check_database(
        database,
        n_train=3696,
        n_dev_references=168,
        n_dev_references_samples=8,
        n_dev_probes=336,
        n_dev_probes_samples=1,
    )


def test_voxforge():
    database = SpearBioDatabase(
        "voxforge", protocol="Default", data_path="dummy/"
    )

    _check_database(
        database,
        n_train=3148,
        n_dev_references=10,
        n_dev_references_samples=None,  # Variable sample count
        n_dev_probes=300,
        n_dev_probes_samples=1,
        n_eval_references=10,
        n_eval_references_samples=None,  # Variable sample count
        n_eval_probes=300,
        n_eval_probes_samples=1,
    )


def test_nist_sre04to16():
    database = SpearBioDatabase(
        "nist_sre04to16", protocol="core", data_path="dummy/"
    )

    _check_database(
        database,
        n_train=71728,
        n_dev_references=80,
        n_dev_references_samples=None,  # Variable sample count
        n_dev_probes=1207,
        n_dev_probes_samples=1,
        n_eval_references=802,
        n_eval_references_samples=None,  # Variable sample count
        n_eval_probes=9294,
        n_eval_probes_samples=1,
    )
