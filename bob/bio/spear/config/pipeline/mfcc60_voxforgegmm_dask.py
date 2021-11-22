#!/usr/bin/env python
# @author: Yannick Dayer <yannick.dayer@idiap.ch>
# @date: Fri 02 Jul 2021 15:41:48 UTC+02

from .mfcc60_voxforgegmm import pipeline
from bob.pipelines import wrap, ToDaskBag
from bob.bio.gmm.bioalgorithm.GMM import GMMDaskWrapper
from sklearn.pipeline import Pipeline
from bob.bio.base.pipelines.vanilla_biometrics.wrappers import BioAlgorithmDaskWrapper
from bob.extension import rc

annotator = pipeline.transformer.steps[0][1]
extractor = pipeline.transformer.steps[1][1]
algorithm = pipeline.transformer.steps[2][1]

annotator = wrap(["dask"], annotator)
extractor = wrap(["checkpoint", "dask"], extractor, features_dir=f"{rc['temp']}/features")
algorithm = wrap([GMMDaskWrapper], algorithm.estimator)

transformer = Pipeline(
    [
        ("to-bags", ToDaskBag(npartitions=10)),
        (
            "annotator",
            annotator,
        ),
        ("extractor", extractor),
        ("algorithm", algorithm),
    ]
)
pipeline.transformer = transformer
pipeline.biometric_algorithm = BioAlgorithmDaskWrapper(pipeline.biometric_algorithm)


def _write_scores(scores):
    return scores.map_partitions(pipeline.write_scores_on_dask)


pipeline.write_scores_on_dask = pipeline.write_scores
pipeline.write_scores = _write_scores
