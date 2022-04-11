#!/usr/bin/env python
# @author: Yannick Dayer <yannick.dayer@idiap.ch>
# @date: Thu 31 Mar 2022 16:56:40 UTC+02

from sklearn.pipeline import Pipeline

from bob.bio.base.pipelines import PipelineSimple
from bob.bio.spear.algorithm import ISV, ReferenceIdEncoder
from bob.bio.spear.annotator import Energy_2Gauss
from bob.bio.spear.extractor import Cepstral
from bob.pipelines import wrap

bioalgorithm = ISV(
    # ISV parameters
    subspace_dimension_of_u=50,
    training_iterations=5,
    # GMM parameters
    ubm_n_gaussians=256,
    ubm_training_iterations=5,
    ubm_training_threshold=0.0,  # Maximum number of iterations as stopping criterion
    ubm_kmeans_training_iterations=5,
    ubm_kmeans_init_iterations=5,
    ubm_kmeans_oversampling_factor=64,
    rng=0,
)

transformer = Pipeline(
    [
        ("annotator", wrap([Energy_2Gauss, "sample"])),
        ("extractor", wrap([Cepstral, "sample"])),
        ("reference_id_encoder", wrap([ReferenceIdEncoder, "sample"])),
        ("algorithm_trainer", wrap(["sample"], bioalgorithm)),
    ]
)

pipeline = PipelineSimple(transformer, bioalgorithm)
