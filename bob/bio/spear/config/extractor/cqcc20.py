import bob.bio.spear
import numpy

cqcc20 = bob.bio.spear.extractor.CQCCFeatures(
    features_mask=numpy.r_[numpy.arrange(0, 20), numpy.arrange(30, 50), numpy.arrange(60, 80)])
