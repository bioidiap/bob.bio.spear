#!/usr/bin/env python
# @author: Yannick Dayer <yannick.dayer@idiap.ch>
# @date: Fri 02 Jul 2021 15:41:48 UTC+02

from sklearn.pipeline import Pipeline

from bob.bio.base.pipelines import PipelineSimple
from bob.bio.spear.algorithm import GMM
from bob.bio.spear.annotator import Mod_4Hz
from bob.bio.spear.extractor import Cepstral
from bob.pipelines import wrap

bioalgorithm = GMM(
    number_of_gaussians=512,
    ubm_training_iterations=25,
    kmeans_training_iterations=25,
    gmm_enroll_iterations=1,
    training_threshold=0.0,  # Maximum number of iterations as stopping criterion
    kmeans_init_iterations=5,
    kmeans_oversampling_factor=128,
    init_seed=2,
)

transformer = Pipeline(
    [
        ("annotator", wrap(["sample"], Mod_4Hz())),
        ("extractor", wrap(["sample"], Cepstral())),
        ("algorithm_trainer", wrap(["sample"], bioalgorithm)),
    ]
)

pipeline = PipelineSimple(transformer, bioalgorithm)
database = "mobio-audio-male"
