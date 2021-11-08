#!/usr/bin/env python
# @author: Yannick Dayer <yannick.dayer@idiap.ch>
# @date: Fri 02 Jul 2021 15:41:48 UTC+02

from sklearn.pipeline import Pipeline

from bob.bio.base.pipelines.vanilla_biometrics import VanillaBiometricsPipeline
from bob.bio.gmm.bioalgorithm import GMM
from bob.bio.spear.extractor import Cepstral
from bob.pipelines import wrap
from bob.pipelines.sample_loaders import AnnotationsLoader

annotations_loader = AnnotationsLoader(
    annotation_directory="results~/annotations",
)

# Map the Sample input attributes to the parameters of the tranform method.
# (`data` of Sample already mapped to the first positional arg by default)
wrapped_extractor_transformer = wrap(
    ["sample"],
    Cepstral(),
    transform_extra_arguments=[("sample_rate", "rate"), ("vad_labels", "annotations")],
)

bioalgorithm = GMM(
    number_of_gaussians=256,
    ubm_training_iterations=5,
    gmm_enroll_iterations=1,
    training_threshold=0.0,  # Maximum number of iterations as stopping criterion
)

transformer = Pipeline(
    [
        ("extractor", wrapped_extractor_transformer),
        ("algorithm", wrap(["sample"], bioalgorithm)),
    ]
)

pipeline = VanillaBiometricsPipeline(transformer, bioalgorithm)
