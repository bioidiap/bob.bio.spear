#!/usr/bin/env python

import bob.bio.spear

algorithm = bob.bio.spear.algorithm.GMM(
    number_of_gaussians=128,
)
