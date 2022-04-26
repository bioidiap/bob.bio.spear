#!/usr/bin/env python
# @author: Yannick Dayer <yannick.dayer@idiap.ch>
# @date: Thu 31 Mar 2022 16:56:40 UTC+02

from sklearn.pipeline import Pipeline

from bob.bio.base.pipelines import PipelineSimple
from bob.bio.spear.algorithm import ISV, ReferenceIdEncoder, LabelRepeater
from bob.bio.spear.annotator import Energy_2Gauss
from bob.bio.spear.extractor import Cepstral
from bob.pipelines import wrap

bioalgorithm = ISV(
    # ISV parameters
    subspace_dimension_of_u=2,
    # GMM parameters
    number_of_gaussians=8,
    ubm_training_iterations=2,
    kmeans_training_iterations=2,
    gmm_enroll_iterations=1,
    training_threshold=1e-3,  # Maximum number of iterations as stopping criterion
    kmeans_init_iterations=5,
    kmeans_oversampling_factor=32,
    rng=0,
)

transformer = Pipeline(
    [
        ("annotator", wrap([Energy_2Gauss, "sample"])),
        ("extractor", wrap([Cepstral, "sample"])),
        ("reference_id_encoder", wrap([ReferenceIdEncoder, "sample"])),
        ("label_repeater", LabelRepeater(data_attr="data", label_attr="reference_id_int")),
        ("algorithm_trainer", wrap(["sample"], bioalgorithm)),
    ]
)

pipeline = PipelineSimple(transformer, bioalgorithm)
