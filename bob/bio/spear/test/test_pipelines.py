"""Tests for pipelines default configurations."""

from sklearn.pipeline import Pipeline as SklearnPipeline

from bob.bio.base import load_resource
from bob.bio.base.algorithm import GMM
from bob.bio.base.pipelines import PipelineSimple
from bob.bio.base.test.utils import is_library_available
from bob.learn.em import IVectorMachine


@is_library_available("torchaudio")
def test_mfcc_gmm_voxforge():
    """Creating the gmm-voxforge pipeline."""
    pipeline = load_resource("gmm-voxforge", "pipeline")
    assert isinstance(pipeline, PipelineSimple)
    assert isinstance(pipeline.transformer, SklearnPipeline)
    assert isinstance(pipeline.biometric_algorithm, GMM)


# @is_library_available("torchaudio")
def test_mfcc_gmm_mobio():
    """Creating the gmm-mobio pipeline."""
    config_module = load_resource("gmm-mobio", "config", "bob.bio.spear")
    pipeline = config_module.pipeline
    assert isinstance(pipeline, PipelineSimple)
    assert isinstance(pipeline.transformer, SklearnPipeline)
    assert isinstance(pipeline.biometric_algorithm, GMM)


@is_library_available("torchaudio")
def test_mfcc_isv_voxforge():
    """Creating the isv-voxforge pipeline."""
    pipeline = load_resource("isv-voxforge", "pipeline")
    assert isinstance(pipeline, PipelineSimple)
    assert isinstance(pipeline.transformer, SklearnPipeline)


@is_library_available("torchaudio")
def test_mfcc_ivector():
    """Creating the IVector pipeline."""
    pipeline = load_resource("ivector-default", "pipeline")
    assert isinstance(pipeline, PipelineSimple)
    assert isinstance(pipeline.transformer, SklearnPipeline)
    assert isinstance(
        pipeline.transformer.steps[-1][1].estimator, IVectorMachine
    )
