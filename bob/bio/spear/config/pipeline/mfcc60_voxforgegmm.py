#!/usr/bin/env python
# @author: Yannick Dayer <yannick.dayer@idiap.ch>
# @date: Fri 02 Jul 2021 15:41:48 UTC+02

import os.path

from sklearn.pipeline import Pipeline

from bob.bio.base.pipelines.vanilla_biometrics import BioAlgorithmLegacy
from bob.bio.base.pipelines.vanilla_biometrics import VanillaBiometricsPipeline
from bob.bio.base.pipelines.vanilla_biometrics.legacy import get_temp_directory
from bob.bio.base.transformers import AlgorithmTransformer
from bob.bio.gmm.algorithm import GMM
from bob.bio.spear.extractor import Cepstral
from bob.pipelines import wrap
from bob.pipelines.sample_loaders import AnnotationsLoader

temp_dir = get_temp_directory("spear_mfcc60_voxforgegmm")

print(f"temp_dir is {temp_dir}")

annotations_loader = AnnotationsLoader(
    annotation_directory="results~/annotations",
)
extractor_transformer = Cepstral()

legacy_algorithm = GMM(
    number_of_gaussians=256,
    training_threshold=0.0,  # Maximum number of iterations as stopping criterion
)

algorithm_transformer = wrap(
    ["sample"],
    AlgorithmTransformer(
        legacy_algorithm, projector_file=os.path.join(temp_dir, "projector.hdf5")
    ),
)

transformer = Pipeline(
    [
        ("extractor", extractor_transformer),
        ("algorithm_transformer", algorithm_transformer),
    ]
)

algorithm = BioAlgorithmLegacy(
    legacy_algorithm,
    base_dir=temp_dir,
    projector_file=os.path.join(temp_dir, "projector.hdf5"),
)

pipeline = VanillaBiometricsPipeline(transformer, algorithm)
