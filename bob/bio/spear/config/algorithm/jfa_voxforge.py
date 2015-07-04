#!/usr/bin/env python

import bob.bio.gmm
import numpy

algorithm = bob.bio.gmm.algorithm.JFA(
  # JFA Training
  subspace_dimension_of_u = 10, # U subspace dimension
  subspace_dimension_of_v = 5, # V subspace dimension
  jfa_training_iterations = 10, # Number of EM iterations for the JFA training
  # GMM training
  number_of_gaussians = 256,
  training_threshold = 0.0,
)
