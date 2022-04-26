#!/usr/bin/env python

import bob.bio.spear

algorithm = bob.bio.spear.algorithm.GMM(
    number_of_gaussians=256,
    training_threshold=0.0,  # This ensure the use of maximum number of iterations as stopping criterion
)
