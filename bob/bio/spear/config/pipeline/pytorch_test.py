#!/usr/bin/env python
# @author: Yannick Dayer <yannick.dayer@idiap.ch>
# @date: Thu 12 Jan 2023 09:31:53 UTC+01

"""Creates a biometric PipelineSimple for the `bob bio pipeline simple` command.

This is a test pipeline for the pytorch embedding extractor.

This pipeline is composed of the following steps:
    - extractor: Pytorch embedding using TODO model
    - algorithm: Distance (cosine? TODO)
"""

from sklearn.pipeline import Pipeline

from bob.bio.base.algorithm import Distance
from bob.bio.base.pipelines import PipelineSimple
from bob.bio.spear.extractor import PyTorchModel
from bob.pipelines import wrap

# Transformer part of PipelineSimple
transformer = Pipeline(
    [
        (
            "extractor",
            wrap(["sample"], PyTorchModel("PATH_TO_CHECKPOINT_FILE")),
        ),  # TODO
    ]
)

# PipelineSimple instance used by `execute_pipeline_simple` or the `pipeline simple` command
pipeline = PipelineSimple(transformer, Distance())
