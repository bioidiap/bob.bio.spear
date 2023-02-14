import os

import numpy as np
import pkg_resources

from h5py import File as HDF5File

from bob.bio.spear.audio_processing import (
    cepstral,
    energy,
    read,
    resample,
    spectrogram,
)

TEST_DATA_FOLDER = pkg_resources.resource_filename(__name__, "data")
WAV_PATH = os.path.join(TEST_DATA_FOLDER, "sample.wav")
DATA_PATH = os.path.join(TEST_DATA_FOLDER, "sample.hdf5")
GENERATE_REFS = False
with HDF5File(DATA_PATH, "r") as f:
    DATA = f["data"][()]
    RATE = f["rate"][()]


def test_read():
    data, sr = read(WAV_PATH)
    assert isinstance(data, np.ndarray)
    assert data.shape == (77760,)  # Number of samples in samples.wav
    assert data.dtype == np.float32
    assert data[0] == 33.0  # First audio sample value of sample.wav
    assert sr == 16000  # Sample rate of sample.wav

    # Loading with a set sample rate
    data, sr = read(WAV_PATH, channel=0, force_sample_rate=8000)
    assert isinstance(data, np.ndarray)
    assert data.shape == (38880,)
    assert data.dtype == np.float32
    assert sr == 8000


def test_resample():
    resampled = resample(DATA, RATE, 41100)
    assert isinstance(resampled, np.ndarray)
    assert resampled.shape == (199746,)
    assert resampled.dtype == np.float32


def _assert_allclose(actual, reference, **kwargs):
    rtol = kwargs.pop("rtol", 1e-07)
    atol = kwargs.pop("atol", 1e-05)
    np.testing.assert_allclose(
        actual, reference, rtol=rtol, atol=atol, **kwargs
    )


def test_energy():
    audio_energy = energy(
        DATA,
        RATE,
        win_length_ms=20,
        win_shift_ms=10,
    )

    ref_path = os.path.join(TEST_DATA_FOLDER, "sample_energy.npy")
    if GENERATE_REFS:
        np.save(ref_path, audio_energy, allow_pickle=False)
    ref = np.load(ref_path)

    _assert_allclose(audio_energy, ref)


def test_spectrogram():

    spec = spectrogram(
        DATA,
        RATE,
        win_length_ms=20,
        win_shift_ms=10,
        n_filters=20,
        f_min=0.0,
        f_max=4000.0,
        pre_emphasis_coef=1.0,
        mel_scale=True,
    )

    ref_path = os.path.join(TEST_DATA_FOLDER, "sample_spectrogram.npy")
    if GENERATE_REFS:
        np.save(ref_path, spec, allow_pickle=False)
    ref = np.load(ref_path)

    _assert_allclose(spec, ref)


def test_cepstral():

    cep = cepstral(
        DATA,
        RATE,
        win_length_ms=20,
        win_shift_ms=10,
        n_filters=20,
        f_min=0.0,
        f_max=4000.0,
        pre_emphasis_coef=1.0,
        mel_scale=True,
        n_ceps=20,
        delta_win=2,
        dct_norm=True,
        with_energy=True,
        with_delta=True,
        with_delta_delta=True,
    )

    ref_path = os.path.join(TEST_DATA_FOLDER, "sample_cepstral.npy")
    if GENERATE_REFS:
        np.save(ref_path, cep, allow_pickle=False)
    ref = np.load(ref_path)

    _assert_allclose(cep, ref)
