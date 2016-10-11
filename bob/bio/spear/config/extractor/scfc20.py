
import bob.bio.spear.extractor

extractor = bob.bio.spear.extractor.CepstralExtended(
    # the parameters are as specified in the paper "A Comparison of Features for Synthetic Speech Detection" by
    # Md Sahidullah, Tomi Kinnunen, Cemal Hanilci
    # SCFC features as per paper that compares different features

    pre_emphasis_coef=0.97, # as per the algorithm implemented in the paper
    n_ceps=20, # number of SCFC coefficients should be 20 - this is the number we cut off from whole Cepstrum
    n_filters=20, # number of filters in the bank is also 20
    win_length_ms=20.,  # 20 ms - this is the value in the paper
    win_shift_ms=10.,  # This is the overlap - half of the window
    f_max=8000,  # this number insures we take half of the frequencies after FFT - so we retain only 257 values for 512 window
    mel_scale=False,
    with_delta=True,  # As reported in the paper
    with_delta_delta=True,  # As reported in the paper
    rect_filter=True, # in the paper, these features are computed with a rectangular filter
    scfc_features=True,
    log_filter=False, # it is important to set it to False, so no log is applied to SCFC features
    # energy_filter =True, # The paper DOES NOT use power of FFT magnitude for SCMC and SCFC features
    delta_win=1, # the paper computes deltas on window of size 1
)

