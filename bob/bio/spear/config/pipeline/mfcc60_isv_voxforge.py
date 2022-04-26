#!/usr/bin/env python
# @author: Yannick Dayer <yannick.dayer@idiap.ch>
# @date: Thu 31 Mar 2022 16:56:40 UTC+02

from sklearn.pipeline import Pipeline

from bob.bio.base.pipelines import PipelineSimple
from bob.bio.spear.algorithm import ISV, ReferenceIdEncoder, LabelRepeater
from bob.bio.spear.annotator import Energy_2Gauss
from bob.bio.spear.extractor import Cepstral
from bob.pipelines import wrap
from bob.learn.em import KMeansMachine


SEED = 0

bioalgorithm = ISV(
    # ISV parameters
    r_U=50,
    random_state=SEED,
    # GMM parameters
    ubm_kwargs=dict(
        n_gaussians=256,
        max_fitting_steps=2,
        enroll_iterations=1,
        convergence_threshold=1e-3,  # Maximum number of iterations as stopping criterion
        k_means_trainer=KMeansMachine(
            n_clusters=256,
            max_iter=2,
            random_state=SEED,
            init_max_iter=5,
            oversampling_factor=64,
        ),
    ),
)

transformer = Pipeline(
    [
        ("annotator", Energy_2Gauss()),
        ("extractor", Cepstral()),
        ("reference_id_encoder", ReferenceIdEncoder()),
        ("label_repeater", LabelRepeater(data_attr="data", label_attr="reference_id_int")),
        ("algorithm_trainer", bioalgorithm),
    ]
)
transformer = wrap(["sample"], transformer)

pipeline = PipelineSimple(transformer, bioalgorithm)
