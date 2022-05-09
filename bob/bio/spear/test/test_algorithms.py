#!/usr/bin/env python
# @author: Yannick Dayer <yannick.dayer@idiap.ch>
# @date: Wed 23 Mar 2022 11:21:11 UTC+01

"""Tests the configured bioalgorithms."""

import numpy as np

from pkg_resources import resource_filename

from bob.bio.base import load_resource
from bob.bio.spear.algorithm import GMM
from bob.bio.spear.transformer import WavToSample
from bob.learn.em import GMMMachine
from bob.pipelines import Sample


def test_gmm():
    """Loading and running the GMM bioalgorithm."""
    audio_path = resource_filename("bob.bio.spear.test", "data/sample.wav")
    sample = WavToSample().transform([Sample(data=audio_path)])[0]

    # Test setup and config
    pipeline = load_resource("gmm-voxforge", "pipeline")
    transformer = pipeline.transformer
    algorithm = pipeline.biometric_algorithm
    assert isinstance(algorithm, GMM)

    # Try fitting the algorithm
    transformer.fit([sample])
    assert isinstance(algorithm.means, np.ndarray)

    extracted_feature = transformer.transform([sample])[0]

    # Test enrollment
    model = algorithm.enroll(extracted_feature.data)
    assert isinstance(model, GMMMachine)

    # Test scoring
    score = algorithm.score(model, extracted_feature.data)
    assert score.shape == (1,)
    assert score[0] > 0.0
    scores = algorithm.score_multiple_biometric_references(
        [model, model], extracted_feature.data
    )
    assert scores.shape == (2, 1)
