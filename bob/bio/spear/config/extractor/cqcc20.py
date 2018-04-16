import bob.bio.spear
import numpy

# The authors of CQCC features recommend to use only first 20 features, plus deltas and delta-deltas
# feature vector is 60 in this case
cqcc20 = bob.bio.spear.extractor.CQCCFeatures(
    features_mask=numpy.r_[numpy.arange(0, 20), numpy.arange(30, 50), numpy.arange(60, 80)])
