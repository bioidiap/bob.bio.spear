#!/usr/bin/env python
# @author: Yannick Dayer <yannick.dayer@idiap.ch>
# @date: Mon 24 Oct 2022 14:45:33 UTC+02
"""Creates a biometric PipelineSimple for the `bob bio pipeline simple` command.

This pipeline is composed of the following steps:
    - annotator: Energy_2Gauss (VAD on 2 Gaussians)
    - extractor: Cepstral (MFCC, 60 features)
    - projector: IVector
    - algorithm: PLDA from speechbrain
"""

from sklearn.pipeline import Pipeline

from bob.bio.base.algorithm import GMM
from bob.bio.base.pipelines import PipelineSimple
from bob.bio.spear.algorithm import PLDA
from bob.bio.spear.annotator import Energy_2Gauss
from bob.bio.spear.extractor import Cepstral
from bob.learn.em import IVectorMachine, KMeansMachine  # , Whitening
from bob.pipelines import wrap

# Number of Gaussians for the UBM (used by kmeans and GMM)
n_gaussians = 12

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

ivector_transformer = IVectorMachine(ubm=ubm, dim_t=8, max_iterations=8)


# class LenghtNorm(BaseEstimator):
#     def transform(self, X):
#         return [x / numpy.linalg.norm(x) for x in X]

#     def _more_tags(self):
#         return {"requires_fit": False}

plda = PLDA(rank_f=5)

# Transformer part of PipelineSimple
transformer = Pipeline(
    [
        ("annotator", Energy_2Gauss()),
        ("extractor", Cepstral()),
        ("ubm", ubm),
        # ("reference_id_encoder", ReferenceIdEncoder()),
        ("ivector", ivector_transformer),
        # ("whitening", Whitening()),
        ("plda_trainer", plda),
    ]
)


transformer = wrap(["sample"], transformer)

bio_algorithm = plda

# PipelineSimple instance used by `execute_pipeline_simple` or the `pipeline simple` command
pipeline = PipelineSimple(transformer, bio_algorithm)
