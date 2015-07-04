#!/usr/bin/env python

import bob.bio.gmm
import numpy

algorithm = bob.bio.gmm.algorithm.GMM(
    number_of_gaussians = 128,
)

