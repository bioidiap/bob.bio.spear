#!/usr/bin/env python
# @author: Yannick Dayer <yannick.dayer@idiap.ch>
# @date: Thu 31 Mar 2022 16:56:40 UTC+02

from sklearn.pipeline import Pipeline

from bob.bio.base.algorithm import GMM, ISV
from bob.bio.base.pipelines import PipelineSimple
from bob.bio.spear.annotator import Energy_2Gauss
from bob.bio.spear.extractor import Cepstral
from bob.bio.spear.transformer import ReferenceIdEncoder
from bob.learn.em import KMeansMachine
from bob.pipelines import wrap

SEED = 0

ubm = GMM(
    n_gaussians=8,
    max_fitting_steps=2,
    convergence_threshold=1e-3,  # Maximum number of iterations as stopping criterion
    k_means_trainer=KMeansMachine(
        n_clusters=8,
        max_iter=2,
        random_state=SEED,
        init_max_iter=5,
        oversampling_factor=64,
    ),
    return_stats_in_transform=True,
)

bioalgorithm = ISV(
    # ISV parameters
    r_U=2,
    random_state=SEED,
    em_iterations=2,
    enroll_iterations=1,
    # GMM parameters
    ubm=ubm,
)

transformer = Pipeline(
    [
        ("annotator", Energy_2Gauss()),
        ("extractor", Cepstral()),
        ("ubm", ubm),
        ("template_id_encoder", ReferenceIdEncoder()),
        ("isv", bioalgorithm),
    ]
)
transformer = wrap(["sample"], transformer)

pipeline = PipelineSimple(transformer, bioalgorithm)
