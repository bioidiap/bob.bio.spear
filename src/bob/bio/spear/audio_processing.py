#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Elie Khoury <Elie.Khoury@idiap.ch>
# Andre Anjos <andre.anjos@idiap.ch>
# Pavel Korshunov <Pavel.Korshunov@idiap.ch>
# Amir Mohammadi <amir.mohammadi@idiap.ch>

import importlib
import logging
import math
import sys

from typing import Optional, Tuple, Union

import numpy
import torch

logger = logging.getLogger(__name__)


def fft(src, dst=None):
    out = numpy.fft.fft(src)
    if dst is not None:
        dst[:] = out
    return out


def init_hamming_kernel(win_length):
    # Hamming initialization
    cst = 2 * math.pi / (win_length - 1.0)
    hamming_kernel = numpy.zeros(win_length)

    for i in range(win_length):
        hamming_kernel[i] = 0.54 - 0.46 * math.cos(i * cst)
    return hamming_kernel


def init_freqfilter(rate, win_size, mel_scale, n_filters, f_min, f_max):
    # Compute cut-off frequencies
    p_index = numpy.array(numpy.zeros(n_filters + 2), dtype=numpy.float64)
    if mel_scale:
        # Mel scale
        m_max = mel_python(f_max)
        m_min = mel_python(f_min)

        for i in range(n_filters + 2):
            alpha = float(i) / (n_filters + 1)
            f = mel_inv_python(m_min * (1 - alpha) + m_max * alpha)
            factor = float(f) / rate
            p_index[i] = win_size * factor
    else:
        # linear scale
        for i in range(n_filters + 2):
            alpha = float(i) / (n_filters + 1)
            f = f_min * (1.0 - alpha) + f_max * alpha
            p_index[i] = float(win_size) / rate * f
    return p_index


def init_dct_kernel(n_filters, n_ceps, dct_norm):
    dct_kernel = numpy.zeros([n_ceps, n_filters], dtype=numpy.float64)

    dct_coeff = 1.0
    if dct_norm:
        dct_coeff = math.sqrt(2.0 / n_filters)

    for i in range(0, n_ceps):
        for j in range(0, n_filters):
            dct_kernel[i][j] = dct_coeff * math.cos(
                math.pi * i * (j + 0.5) / float(n_filters)
            )

    if dct_norm:
        column_multiplier = numpy.ones(n_ceps, dtype=numpy.float64)
        column_multiplier[0] = math.sqrt(
            0.5
        )  # first element sqrt(0.5), the rest are 1.
        for j in range(0, n_filters):
            dct_kernel[:, j] = column_multiplier * dct_kernel[:, j]

    return dct_kernel


def resample(
    audio: Union[numpy.ndarray, torch.Tensor],
    rate: int,
    new_rate: int,
    **kwargs,
) -> Union[numpy.ndarray, torch.Tensor]:
    """Resamples the audio to a new sample rate.

    Parameters
    ----------
    audio:
        The audio to resample.
    rate:
        The original sample rate of the audio.
    new_rate:
        The wanted sample rate of the output audio.
    kwargs:
        Arguments passed to :py:class:``torchaudio.transforms.Resample``.
    """

    import torchaudio

    if rate == new_rate:
        return audio

    was_numpy = False
    if isinstance(audio, numpy.ndarray):
        audio = torch.from_numpy(audio)
        was_numpy = True

    resampler = torchaudio.transforms.Resample(
        rate, new_rate, dtype=torch.float32, **kwargs
    )
    audio = resampler(audio)

    return audio.numpy() if was_numpy else audio


def read(
    filename: str,
    channel: Optional[int] = None,
    force_sample_rate: Optional[int] = None,
) -> Tuple[numpy.ndarray, int]:
    """Reads audio file and returns the signal and the sampling rate

    Parameters
    ----------
    filename:
        The full path to the audio file to load.
    channel:
        The channel to load. If None, all channels will be loaded and returned in a 2D
        array in the shape (n_channels, n_samples).
    force_sample_rate:
        If specified, the audio will be resampled to the specified rate. Otherwise, the
        sample rate of the file will be used.

    Returns
    -------
    signal and sampling rate
        The signal in int16 range (-32768 to 32767) and float32 format, and the
        sampling rate in Hz.
    """

    import torchaudio

    try:
        importlib.__import__(
            "soundfile"
        )  # Try to import missing soundfile may throw an OSError.
        torchaudio.set_audio_backend("soundfile")  # May throw a RuntimeError.
    except (RuntimeError, OSError) as e:
        logger.warning(
            "'soundfile' could not be imported or specified as torchaudio "
            "backend. torchaudio may have trouble loading '.sph' files."
        )
        logger.info("error was %s", e)

    data, rate = torchaudio.load(str(filename))

    if channel is not None:
        data = data[channel]
    else:
        if data.ndim > 1:
            data = data[0]

    if force_sample_rate is not None:
        data = resample(data, rate, force_sample_rate)
        rate = force_sample_rate

    # Expected data is in float32 format and int16 range (-32768. to 32767.)
    data = data.numpy().astype(numpy.float32) * 32768

    return data, rate


def audio_info(filename: str):
    """Returns the audio info of a file.

    Parameters
    ----------
    filename:
        The full path to the audio file to load.

    Returns
    -------
    info: torchaudio.backend.common.AudioMetaData
        A dictionary containing the audio information.
    """

    import torchaudio

    return torchaudio.info(str(filename))


def compare(v1, v2, width):
    return abs(v1 - v2) <= width


def mel_python(f):
    return 2595.0 * math.log10(1.0 + f / 700.0)


def mel_inv_python(value):
    return 700.0 * (10 ** (value / 2595.0) - 1)


def sig_norm(win_length, frame, flag):
    gain = 0.0
    for i in range(win_length):
        gain = gain + frame[i] * frame[i]

    ENERGY_FLOOR = 1.0
    if gain < ENERGY_FLOOR:
        gain = math.log(ENERGY_FLOOR)
    else:
        gain = math.log(gain)

    if flag and gain != 0.0:
        for i in range(win_length):
            frame[i] = frame[i] / gain
    return gain


def pre_emphasis(frame, win_shift, coef, last_frame_elem):

    if (coef <= 0.0) or (coef > 1.0):
        print("Error: The emphasis coeff. should be between 0 and 1")
        return None

    last_element = frame[win_shift - 1]
    return (
        numpy.append(
            frame[0] - coef * last_frame_elem, frame[1:] - coef * frame[:-1]
        ),
        last_element,
    )


def hamming_window(vector, hamming_kernel, win_length):
    for i in range(win_length):
        vector[i] = vector[i] * hamming_kernel[i]
    return vector


def log_filter_bank(frame, n_filters, p_index, win_size, energy_filter):
    x1 = numpy.array(frame, dtype=numpy.complex128)
    complex_ = fft(x1)
    abscomplex = numpy.absolute(complex_)
    half_frame = abscomplex[0 : int(win_size / 2) + 1]

    if energy_filter:
        # Energy is basically magnitude in power of 2
        half_frame = half_frame**2

    frame[0 : int(win_size / 2) + 1] = half_frame
    filters = log_triangular_bank(frame, n_filters, p_index)
    return filters, frame


def log_triangular_bank(data, n_filters, p_index):
    res_ = numpy.zeros(n_filters, dtype=numpy.float64)

    denominator = 1.0 / (
        p_index[1 : n_filters + 2] - p_index[0 : n_filters + 1]
    )

    for i in range(0, n_filters):
        li = int(math.floor(p_index[i] + 1))
        mi = int(math.floor(p_index[i + 1]))
        ri = int(math.floor(p_index[i + 2]))
        if i == 0 or li == ri:
            li -= 1

        vec_left = numpy.arange(li, mi + 1)
        vec_right = numpy.arange(mi + 1, ri + 1)
        res_[i] = numpy.sum(
            data[vec_left] * denominator[i] * (vec_left - p_index[i])
        ) + numpy.sum(
            data[vec_right] * denominator[i + 1] * (p_index[i + 2] - vec_right)
        )
        # alternative but equivalent implementation:
        # filt = numpy.zeros(ri-li+1, dtype=numpy.float64)
        # filt_l = denominator[i] * (vec_left-p_index[i])
        # filt_p = denominator[i+1] * (p_index[i+2]-vec_right)
        # filt = numpy.append(filt_l, filt_p)
        # vect_full = numpy.arange(li, ri+1)
        # res_[i] = numpy.sum(data[vect_full] * filt)

    FBANK_OUT_FLOOR = sys.float_info.epsilon
    return numpy.log(numpy.where(res_ < FBANK_OUT_FLOOR, FBANK_OUT_FLOOR, res_))


def dct_transform(filters, n_filters, dct_kernel, n_ceps):

    ceps = numpy.zeros(n_ceps)
    vec = numpy.array(range(0, n_filters))
    for i in range(0, n_ceps):
        ceps[i] = numpy.sum(filters[vec] * dct_kernel[i])

    return ceps


def energy(data, rate, *, win_length_ms=20.0, win_shift_ms=10.0):

    #########################
    # Initialisation part ##
    #########################

    win_length = int(rate * win_length_ms / 1000)
    win_shift = int(rate * win_shift_ms / 1000)
    win_size = int(2.0 ** math.ceil(math.log(win_length) / math.log(2)))

    ######################################
    # End of the Initialisation part ###
    ######################################

    ######################################
    #          Core code             ###
    ######################################

    data_size = data.shape[0]
    n_frames = int(1 + (data_size - win_length) / win_shift)

    # create features set

    features = [0 for j in range(n_frames)]

    # compute cepstral coefficients
    for i in range(n_frames):
        # create a frame
        frame = numpy.zeros(win_size, dtype=numpy.float64)
        vec = numpy.arange(win_length)
        frame[vec] = data[vec + i * win_shift]
        som = numpy.sum(frame)
        som = som / win_size
        frame[vec] -= som  # normalization by mean here

        energy = sig_norm(win_length, frame, False)
        features[i] = energy

    return numpy.array(features)


def spectrogram(
    data,
    rate,
    *,
    win_length_ms=20.0,
    win_shift_ms=10.0,
    n_filters=24,
    f_min=0.0,
    f_max=4000.0,
    pre_emphasis_coef=0.95,
    mel_scale=True,
    energy_filter=False,
    log_filter=True,
    energy_bands=False,
):
    #########################
    # Initialisation part ##
    #########################

    win_length = int(rate * win_length_ms / 1000)
    win_shift = int(rate * win_shift_ms / 1000)
    win_size = int(2.0 ** math.ceil(math.log(win_length) / math.log(2)))

    # Hamming initialisation
    hamming_kernel = init_hamming_kernel(win_length)

    # Compute cut-off frequencies
    p_index = init_freqfilter(
        rate, win_size, mel_scale, n_filters, f_min, f_max
    )

    ######################################
    # End of the Initialisation part ###
    ######################################

    ######################################
    #          Core code             ###
    ######################################

    data_size = data.shape[0]
    n_frames = int(1 + (data_size - win_length) / win_shift)

    # create features set
    features = numpy.zeros(
        [n_frames, int(win_size / 2) + 1], dtype=numpy.float64
    )

    last_frame_elem = 0
    # compute cepstral coefficients
    for i in range(n_frames):
        # create a frame
        frame = numpy.zeros(win_size, dtype=numpy.float64)
        vec = numpy.arange(win_length)
        frame[vec] = data[vec + i * win_shift]
        som = numpy.sum(frame)
        som = som / win_size
        frame[vec] -= som  # normalization by mean here

        frame_, last_frame_elem = pre_emphasis(
            frame[vec], win_shift, pre_emphasis_coef, last_frame_elem
        )
        frame[vec] = frame_

        # Hamming windowing
        frame = hamming_window(frame, hamming_kernel, win_length)

        _, spec_row = log_filter_bank(
            frame, n_filters, p_index, win_size, energy_filter
        )

        features[i] = spec_row[0 : int(win_size / 2) + 1]

    return numpy.array(features)


def cepstral(
    data,
    rate,
    *,
    win_length_ms=20,
    win_shift_ms=10,
    n_filters=20,
    f_min=0.0,
    f_max=4000.0,
    pre_emphasis_coef=1.0,
    mel_scale=True,
    n_ceps=19,
    delta_win=2,
    dct_norm=True,
    with_energy=True,
    with_delta=True,
    with_delta_delta=True,
):

    #########################
    # Initialisation part ##
    #########################

    win_length = int(rate * win_length_ms / 1000)
    win_shift = int(rate * win_shift_ms / 1000)
    win_size = int(2.0 ** math.ceil(math.log(win_length) / math.log(2)))

    # Hamming initialisation
    hamming_kernel = init_hamming_kernel(win_length)

    # Compute cut-off frequencies
    p_index = init_freqfilter(
        rate,
        win_size,
        mel_scale,
        n_filters,
        f_min,
        f_max,
    )

    # Cosine transform initialisation
    dct_kernel = init_dct_kernel(n_filters, n_ceps, dct_norm)

    ######################################
    # End of the Initialisation part ###
    ######################################

    ######################################
    #          Core code             ###
    ######################################

    data_size = data.shape[0]
    n_frames = int(1 + (data_size - win_length) / win_shift)

    # create features set
    dim0 = n_ceps
    if with_energy:
        dim0 += +1
    dim = dim0
    if with_delta:
        dim += dim0
        if with_delta_delta:
            dim += dim0
    else:
        with_delta_delta = False

    features = numpy.zeros([n_frames, dim], dtype=numpy.float64)

    last_frame_elem = 0
    # compute cepstral coefficients
    for i in range(n_frames):
        # create a frame
        frame = numpy.zeros(win_size, dtype=numpy.float64)
        vec = numpy.arange(win_length)
        frame[vec] = data[vec + i * win_shift]
        som = numpy.sum(frame)
        som = som / win_size
        frame[vec] -= som  # normalization by mean here

        if with_energy:
            energy = sig_norm(win_length, frame, False)

        # pre-emphasis filtering
        frame_, last_frame_elem = pre_emphasis(
            frame[vec], win_shift, pre_emphasis_coef, last_frame_elem
        )
        frame[vec] = frame_

        # Hamming windowing
        frame = hamming_window(frame, hamming_kernel, win_length)

        # FFT and filters
        filters, _ = log_filter_bank(
            frame, n_filters, p_index, win_size, energy_filter=False
        )

        # apply DCT
        ceps = dct_transform(filters, n_filters, dct_kernel, n_ceps)

        ######################################
        #     Deltas and Delta-Deltas    ###
        ######################################

        d1 = n_ceps
        if with_energy:
            d1 = n_ceps + 1
            ceps = numpy.append(ceps, energy)

        # stock the results in features matrix
        vec = numpy.arange(d1)
        features[i][0:d1] = ceps[vec]

    # compute Delta coefficient
    if with_delta:
        som = 0.0
        for i in range(1, delta_win + 1):
            som = som + i * i
        som = som * 2

        for i in range(n_frames):
            for k in range(n_ceps):
                features[i][d1 + k] = 0.0
                for ll in range(1, delta_win + 1):
                    if i + ll < n_frames:
                        p_ind = i + ll
                    else:
                        p_ind = n_frames - 1
                    if i - ll > 0:
                        n_ind = i - ll
                    else:
                        n_ind = 0
                    features[i][d1 + k] = features[i][d1 + k] + ll * (
                        features[p_ind][k] - features[n_ind][k]
                    )
                # features[i][d1+k] = features[i][d1+k] / som  # do not normalize anymore

    # compute Delta of the Energy
    if with_delta and with_energy:
        som = 0.0

        vec = numpy.arange(1, delta_win + 1)
        som = 2.0 * numpy.sum(vec * vec)

        for i in range(n_frames):
            k = n_ceps
            features[i][d1 + k] = 0.0
            for ll in range(1, delta_win + 1):
                if i + ll < n_frames:
                    p_ind = i + ll
                else:
                    p_ind = n_frames - 1
                if i - ll > 0:
                    n_ind = i - ll
                else:
                    n_ind = 0
                features[i][d1 + k] = features[i][d1 + k] + ll * (
                    features[p_ind][k] - features[n_ind][k]
                )
            # features[i][d1+k] = features[i][d1+k] / som  # do not normalize anymore

    # compute Delta Delta of the coefficients
    if with_delta_delta:
        som = 0.0
        for i in range(1, delta_win + 1):
            som = som + i * i
        som = som * 2
        for i in range(n_frames):
            for k in range(n_ceps):
                features[i][2 * d1 + k] = 0.0
                for ll in range(1, delta_win + 1):
                    if i + ll < n_frames:
                        p_ind = i + ll
                    else:
                        p_ind = n_frames - 1
                    if i - ll > 0:
                        n_ind = i - ll
                    else:
                        n_ind = 0
                    features[i][2 * d1 + k] = features[i][2 * d1 + k] + ll * (
                        features[p_ind][d1 + k] - features[n_ind][d1 + k]
                    )
                # features[i][2*d1+k] = features[i][2*d1+k] / som  # do not normalize anymore

    # compute Delta Delta of the energy
    if with_delta_delta and with_energy:
        som = 0.0
        for i in range(1, delta_win + 1):
            som = som + i * i
        som = som * 2
        for i in range(n_frames):
            k = n_ceps
            features[i][2 * d1 + k] = 0.0
            for ll in range(1, delta_win + 1):
                if i + ll < n_frames:
                    p_ind = i + ll
                else:
                    p_ind = n_frames - 1
                if i - ll > 0:
                    n_ind = i - ll
                else:
                    n_ind = 0
                features[i][2 * d1 + k] = features[i][2 * d1 + k] + ll * (
                    features[p_ind][d1 + k] - features[n_ind][d1 + k]
                )
            # features[i][2*d1+k] = features[i][2*d1+k] / som  # do not normalize anymore

    return numpy.array(features)
