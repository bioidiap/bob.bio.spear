#!/usr/bin/env python
# @author: Yannick Dayer <yannick.dayer@idiap.ch>
# @date: Fri 02 Jul 2021 15:41:48 UTC+02

from sklearn.pipeline import Pipeline

from bob.bio.base.pipelines.vanilla_biometrics import VanillaBiometricsPipeline
from bob.bio.gmm.algorithm import GMM
from bob.bio.spear.annotator.energy_2gauss import Energy_2Gauss
from bob.bio.spear.extractor import Cepstral
from bob.pipelines import wrap

bioalgorithm = GMM(
    number_of_gaussians=8,
    ubm_training_iterations=5,
    kmeans_training_iterations=5,
    gmm_enroll_iterations=1,
    training_threshold=0.0,  # Maximum number of iterations as stopping criterion
    kmeans_init_iterations=5,
    kmeans_oversampling_factor=2,
)

transformer = Pipeline(
    [
        ("annotator", wrap(["sample"], Energy_2Gauss())),
        ("extractor", wrap(["sample"], Cepstral())),
        ("algorithm_trainer", wrap(["sample"], bioalgorithm)),
    ]
)

pipeline = VanillaBiometricsPipeline(transformer, bioalgorithm)
