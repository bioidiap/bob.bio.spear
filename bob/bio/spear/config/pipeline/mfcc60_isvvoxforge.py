#!/usr/bin/env python
# @author: Yannick Dayer <yannick.dayer@idiap.ch>
# @date: Thu 31 Mar 2022 16:56:40 UTC+02

from sklearn.pipeline import Pipeline

from bob.bio.base.pipelines.vanilla_biometrics import VanillaBiometricsPipeline
from bob.bio.spear.algorithm import ISV
from bob.bio.spear.annotator.energy_2gauss import Energy_2Gauss
from bob.bio.spear.extractor import Cepstral
from bob.pipelines import wrap

bioalgorithm = ISV(
    # ISV parameters
    subspace_dimension_of_u=50,
    # GMM parameters
    number_of_gaussians=256,
    ubm_training_iterations=25,
    kmeans_training_iterations=25,
    gmm_enroll_iterations=1,
    training_threshold=0.0,  # Maximum number of iterations as stopping criterion
    kmeans_init_iterations=5,
    kmeans_oversampling_factor=64,
    init_seed=2,
)

transformer = Pipeline(
    [
        ("annotator", wrap([Energy_2Gauss, "sample"])),
        ("extractor", wrap([Cepstral, "sample"])),
        ("algorithm_trainer", wrap(["sample"], bioalgorithm)),
    ]
)

pipeline = VanillaBiometricsPipeline(transformer, bioalgorithm)
