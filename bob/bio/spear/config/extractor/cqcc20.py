import bob.bio.spear
import numpy

cqcc20 = bob.bio.spear.extractor.CQCCFeatures(
    features_mask=numpy.r_[numpy.arange(0, 20), numpy.arange(30, 50), numpy.arange(60, 80)])
