#!/usr/bin/env python

import bob.bio.spear

# GMM training algorithm as per the paper "A Comparison of Features for Synthetic Speech Detection" by
# Md Sahidullah, Tomi Kinnunen, Cemal Hanilci
algorithm = bob.bio.spear.algorithm.GMMRegular(
    number_of_gaussians=512,
    kmeans_training_iterations=10,  # Maximum number of iterations for K-Means
    gmm_training_iterations=10,  # Maximum number of iterations for ML GMM Training
)
