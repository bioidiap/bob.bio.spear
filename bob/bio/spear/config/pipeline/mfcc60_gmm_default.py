#!/usr/bin/env python
# @author: Yannick Dayer <yannick.dayer@idiap.ch>
# @date: Fri 02 Jul 2021 15:41:48 UTC+02

"""Creates a biometric PipelineSimple for the `bob bio pipeline simple` command.

These parameters were chosen to work best with the VoxForge database.

This pipeline is composed of the following steps:
    - annotator: Energy_2Gauss (VAD on 2 Gaussians)
    - extractor: Cepstral (MFCC, 60 features)
    - algorithm: GMM (trained in the pipeline as a Transformer, and used as BioAlgorithm
        for enrollment and scoring)
"""

from sklearn.pipeline import Pipeline

from bob.bio.base.algorithm import GMM
from bob.bio.base.pipelines import PipelineSimple
from bob.bio.spear.annotator import Energy_2Gauss
from bob.bio.spear.extractor import Cepstral
from bob.learn.em import KMeansMachine
from bob.pipelines import wrap

# Number of Gaussians for the UBM (used by kmeans and GMM)
n_gaussians = 256

# Kmeans machine used for GMM initialization
kmeans_trainer = KMeansMachine(
    n_clusters=n_gaussians,
    max_iter=25,
    convergence_threshold=0.0,
    init_max_iter=5,
    oversampling_factor=64,
)

# Algorithm used for enrollment and scoring, trained first as a Transformer.
bioalgorithm = GMM(
    n_gaussians=n_gaussians,
    max_fitting_steps=25,
    enroll_iterations=1,
    convergence_threshold=0.0,  # Maximum number of iterations as stopping criterion
    k_means_trainer=kmeans_trainer,
    random_state=2,
)

# Transformer part of PipelineSimple
transformer = Pipeline(
    [
        ("annotator", wrap(["sample"], Energy_2Gauss())),
        ("extractor", wrap(["sample"], Cepstral())),
        ("algorithm_trainer", wrap(["sample"], bioalgorithm)),
    ]
)


# PipelineSimple instance used by `execute_pipeline_simple` or the `pipeline simple` command
pipeline = PipelineSimple(transformer, bioalgorithm)
