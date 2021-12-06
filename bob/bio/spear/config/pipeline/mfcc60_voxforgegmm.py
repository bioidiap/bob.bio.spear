#!/usr/bin/env python
# @author: Yannick Dayer <yannick.dayer@idiap.ch>
# @date: Fri 02 Jul 2021 15:41:48 UTC+02

from sklearn.pipeline import Pipeline

from bob.bio.base.pipelines.vanilla_biometrics import VanillaBiometricsPipeline
from bob.bio.gmm.bioalgorithm import GMM
from bob.bio.spear.annotator.energy_2gauss import Energy_2Gauss
from bob.bio.spear.extractor import Cepstral
from bob.pipelines import wrap
from bob.pipelines.sample_loaders import AnnotationsLoader

# Loads an annotation file into the `annotations` field
annotations_loader = AnnotationsLoader(
    annotation_directory="./results~/annotations/",
    annotation_extension=".json",
)

bioalgorithm = GMM(
    number_of_gaussians=4, # TODO Set to 256 for full db
    ubm_training_iterations=5,
    gmm_enroll_iterations=1,
    training_threshold=0.0,  # Maximum number of iterations as stopping criterion
)

transformer = Pipeline(
    [
        ("annotations_loader", annotations_loader),
        ("annotator", wrap(["sample"], Energy_2Gauss())),
        ("extractor", wrap(["sample"], Cepstral())),
        ("algorithm", wrap(["sample"], bioalgorithm)),
    ]
)

pipeline = VanillaBiometricsPipeline(transformer, bioalgorithm)
