#!/usr/bin/env python
# @author: Yannick Dayer <yannick.dayer@idiap.ch>
# @date: Wed 23 Mar 2022 11:21:11 UTC+01

"""Tests the configured bioalgorithms."""

import numpy as np

from pkg_resources import resource_filename

from bob.bio.base import load_resource
from bob.bio.base.algorithm import GMM
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

    extracted_feature = transformer.transform([sample])[0].data

    # Test enrollment
    model = algorithm.create_templates([extracted_feature], enroll=True)[0]
    assert isinstance(model, GMMMachine)

    # Test probe template
    probe = algorithm.create_templates([extracted_feature], enroll=False)[0]

    # Test scoring
    scores = algorithm.compare([model], [probe])
    assert scores.shape == (1, 1)
    assert scores[0, 0] > 0.0
