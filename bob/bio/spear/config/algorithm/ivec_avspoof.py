import bob.bio.spear

algorithm = bob.bio.spear.algorithm.IVector(
    # IVector parameters
    subspace_dimension_of_t=100,
    update_sigma=True,
    tv_training_iterations=25,  # Number of EM iterations for the TV training
    # GMM parameters
    number_of_gaussians=256,
    training_threshold=0.0,
    use_lda=True,
    use_wccn=True,
    use_plda=True,
    lda_dim=50,
    plda_dim_F=50,
    plda_dim_G=50,
    plda_training_iterations=200,
)
