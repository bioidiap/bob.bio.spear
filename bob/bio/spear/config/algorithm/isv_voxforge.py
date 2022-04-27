from bob.bio.spear.algorithm import ISV

"""Config file for the ISV algorithm tuned for the Voxforge dataset."""

algorithm = ISV(
    # ISV parameters
    subspace_dimension_of_u=50,
    # GMM parameters
    number_of_gaussians=256,
    training_threshold=0.0,
)
