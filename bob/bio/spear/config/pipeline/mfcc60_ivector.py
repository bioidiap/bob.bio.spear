#!/usr/bin/env python
# @author: Yannick Dayer <yannick.dayer@idiap.ch>
# @date: Wed 24 Aug 2022 18:56:07 UTC+02

"""Creates a biometric PipelineSimple for the `bob bio pipeline simple` command.

This pipeline is composed of the following steps:
    - annotator: Energy_2Gauss (VAD on 2 Gaussians)
    - extractor: Cepstral (MFCC, 60 features)
    - projector: IVector
    - algorithm: Distance
"""

from sklearn.pipeline import Pipeline

from bob.bio.base.algorithm import GMM, Distance
from bob.bio.base.pipelines import PipelineSimple
from bob.bio.spear.annotator import Energy_2Gauss
from bob.bio.spear.extractor import Cepstral
from bob.learn.em import IVectorMachine, KMeansMachine
from bob.pipelines import wrap

# Number of Gaussians for the UBM (used by kmeans and GMM)
n_gaussians = 256

# Kmeans machine used for GMM initialization
kmeans_trainer = KMeansMachine(
    n_clusters=n_gaussians,
    max_iter=25,
    convergence_threshold=1e-6,
    init_max_iter=5,
    oversampling_factor=64,
)

# GMM used as transformer
ubm = GMM(
    n_gaussians=n_gaussians,
    max_fitting_steps=25,
    convergence_threshold=1e-6,
    k_means_trainer=kmeans_trainer,
    random_state=2,
    return_stats_in_transform=True,
)

ivector_transformer = IVectorMachine(ubm=ubm, dim_t=5, max_iterations=16)

# Transformer part of PipelineSimple
transformer = Pipeline(
    [
        ("annotator", wrap(["sample"], Energy_2Gauss())),
        ("extractor", wrap(["sample"], Cepstral())),
        ("ubm", wrap(["sample"], ubm)),
        ("ivector", wrap(["sample"], ivector_transformer)),
    ]
)


# PipelineSimple instance used by `execute_pipeline_simple` or the `pipeline simple` command
pipeline = PipelineSimple(transformer, Distance())
