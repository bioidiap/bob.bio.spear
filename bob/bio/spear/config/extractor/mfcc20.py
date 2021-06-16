import bob.bio.spear.extractor

extractor = bob.bio.spear.extractor.CepstralExtended(
    # the parameters emulate the ones in the paper "A Comparison of Features for Synthetic Speech Detection" by
    # Md Sahidullah, Tomi Kinnunen, Cemal Hanilci
    pre_emphasis_coef=0.97,  # as per the algorithm implemented in the paper
    n_ceps=20,  # number of MFCC coefficients should be 20 - this is the number we cut off from whole Cepstrum
    n_filters=20,  # number of filters in the bank is also 20
    win_length_ms=20.0,  # 20 ms - this is the value in the paper
    win_shift_ms=10.0,  # This is the overlap - half of the window
    f_max=8000,  # this number insures we take half of the frequencies after FFT - so we retain only 257 values for 512 window
    mel_scale=True,  # Mel-scaling is what make these MMFC features
    with_delta=True,  # As reported in the paper
    with_delta_delta=True,  # As reported in the paper
    energy_filter=True,  # The paper uses power of FFT magnitude
    dct_norm=True,  # The paper uses normed DCT-II variant
    delta_win=1,  # the paper computes deltas on window of size 1
)
