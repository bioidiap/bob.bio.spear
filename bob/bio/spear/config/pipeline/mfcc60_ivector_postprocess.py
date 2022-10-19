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

import numpy

from sklearn.base import BaseEstimator
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.pipeline import Pipeline

from bob.bio.base.algorithm import GMM, Distance
from bob.bio.base.pipelines import PipelineSimple
from bob.bio.spear.annotator import Energy_2Gauss
from bob.bio.spear.extractor import Cepstral
from bob.bio.spear.transformer import ReferenceIdEncoder
from bob.learn.em import WCCN, IVectorMachine, KMeansMachine, Whitening
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

ivector_transformer = IVectorMachine(ubm=ubm, dim_t=200, max_iterations=4)


class LengthNorm(BaseEstimator):
    def transform(self, X):
        return [x / numpy.linalg.norm(x) for x in X]

    def _more_tags(self):
        return {"requires_fit": False}


# Transformer part of PipelineSimple
transformer = Pipeline(
    [
        ("annotator", wrap(["sample"], Energy_2Gauss())),
        ("extractor", wrap(["sample"], Cepstral())),
        ("ubm", wrap(["sample"], ubm)),
        ("ivector", wrap(["sample"], ivector_transformer)),
        ("whitening", wrap(["sample"], Whitening())),
        ("length-norm", wrap(["sample"], LengthNorm())),
        ("reference_id_encoder", wrap(["sample"], ReferenceIdEncoder())),
        (
            "lda",
            wrap(
                ["sample"],
                LinearDiscriminantAnalysis(),
                fit_extra_arguments=[("y", "reference_id_int")],
            ),
        ),
        (
            "wccn",
            wrap(
                ["sample"],
                WCCN(),
                fit_extra_arguments=[("y", "reference_id_int")],
            ),
        ),
    ]
)


# PipelineSimple instance used by `execute_pipeline_simple` or the `pipeline simple` command
pipeline = PipelineSimple(transformer, Distance())
