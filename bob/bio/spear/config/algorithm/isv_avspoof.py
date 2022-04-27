import bob.bio.spear

algorithm = bob.bio.spear.algorithm.ISV(
    # ISV parameters
    subspace_dimension_of_u=50,
    # GMM parameters
    number_of_gaussians=256,
    training_threshold=0.0,
)
