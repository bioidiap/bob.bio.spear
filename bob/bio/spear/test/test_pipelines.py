"""Tests for pipelines default configurations."""

import dask.bag.core
import numpy as np

from pkg_resources import load_entry_point
from sklearn.pipeline import Pipeline as SklearnPipeline

from bob.bio.base.algorithm import GMM, ISV
from bob.bio.base.pipelines import PipelineSimple, dask_bio_pipeline
from bob.bio.base.test.utils import is_library_available
from bob.pipelines import Sample, SampleSet


class dummyDatabase:
    """Provides dummy samples to pipelines."""

    def background_model_samples(self):
        """Training set."""
        return [
            Sample(
                data=(np.random.normal(0, 0.2, (16000,)) * 32768).astype(
                    "int32"
                ),
                rate=16000,
                key=id * 10 + s,
                reference_id=str(id),
            )
            for s in range(3)
            for id in range(10)
        ]

    def references(self):
        """Enrollment set."""
        return [
            SampleSet(
                samples=[
                    Sample(
                        data=(
                            np.random.normal(id, 0.1, (16000,)) * 32768
                        ).astype("int32"),
                        rate=16000,
                        key=100 + 10 * id + s,
                        reference_id=str(10 * id),
                    )
                    for s in range(4)
                ]
            )
            for id in range(3)
        ]

    def probes(self):
        """Scoring set."""
        return [
            SampleSet(
                samples=[
                    Sample(
                        data=(
                            np.random.normal(id, 0.1, (16000,)) * 32768
                        ).astype("int32"),
                        rate=16000,
                        key=200 + 10 * id + s,
                        reference_id=str(100 * id),
                    )
                    for s in range(4)
                ]
            )
            for id in range(3)
        ]


def _run_pipeline_on_dummy(pipeline):
    """Executes a PipelineSimple without outputting files."""
    database = dummyDatabase()
    pipeline = dask_bio_pipeline(pipeline)
    result = pipeline(
        database.background_model_samples(),
        database.references(),
        database.probes(),
        score_all_vs_all=True,
    )
    assert isinstance(result, dask.bag.core.Bag)
    result_ = result.compute()
    assert len(result_) == 3
    assert all(len(r) == 3 for r in result_)
    assert all(isinstance(s.data, float) for r in result_ for s in r)


def test_mfcc_gmm_voxforge_config():
    """Creating the gmm-voxforge pipeline."""
    pipeline = load_entry_point(
        "bob.bio.spear", "bob.bio.pipeline", "gmm-voxforge"
    )
    assert isinstance(pipeline, PipelineSimple)
    assert isinstance(pipeline.transformer, SklearnPipeline)
    assert isinstance(pipeline.biometric_algorithm, GMM)


@is_library_available("torchaudio")
def test_mfcc_gmm_voxforge_pipeline():
    """Running the gmm-voxforge pipeline."""
    pipeline = load_entry_point(
        "bob.bio.spear", "bob.bio.pipeline", "gmm-voxforge"
    )
    _run_pipeline_on_dummy(pipeline)


def test_mfcc_gmm_mobio_config():
    """Creating the gmm-mobio pipeline."""
    config_module = load_entry_point(
        "bob.bio.spear", "bob.bio.config", "gmm-mobio"
    )
    pipeline = config_module.pipeline
    assert isinstance(pipeline, PipelineSimple)
    assert isinstance(pipeline.transformer, SklearnPipeline)
    assert isinstance(pipeline.biometric_algorithm, GMM)


@is_library_available("torchaudio")
def test_mfcc_gmm_mobio_pipeline():
    """Running the gmm-mobio pipeline."""
    config_module = load_entry_point(
        "bob.bio.spear", "bob.bio.config", "gmm-mobio"
    )
    pipeline = config_module.pipeline
    _run_pipeline_on_dummy(pipeline)


def test_mfcc_isv_voxforge_config():
    """Creating the isv-voxforge pipeline."""
    pipeline = load_entry_point(
        "bob.bio.spear", "bob.bio.pipeline", "isv-voxforge"
    )
    assert isinstance(pipeline, PipelineSimple)
    assert isinstance(pipeline.transformer, SklearnPipeline)
    assert isinstance(pipeline.biometric_algorithm, ISV)


@is_library_available("torchaudio")
def test_mfcc_isv_voxforge_pipeline():
    """Creating the isv-voxforge pipeline."""
    pipeline = load_entry_point(
        "bob.bio.spear", "bob.bio.pipeline", "isv-voxforge"
    )
    _run_pipeline_on_dummy(pipeline)


def test_mfcc_ivector_config():
    """Creating the IVector pipeline."""
    pipeline = load_entry_point(
        "bob.bio.spear", "bob.bio.pipeline", "ivector-default"
    )
    assert isinstance(pipeline, PipelineSimple)
    assert isinstance(pipeline.transformer, SklearnPipeline)


@is_library_available("torchaudio")
def test_mfcc_ivector_pipeline():
    """Creating the IVector pipeline."""
    pipeline = load_entry_point(
        "bob.bio.spear", "bob.bio.pipeline", "ivector-default"
    )
    _run_pipeline_on_dummy(pipeline)
