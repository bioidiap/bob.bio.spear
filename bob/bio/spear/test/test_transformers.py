#!/usr/bin/env python
# @author: Yannick Dayer <yannick.dayer@idiap.ch>
# @date: Tue 03 May 2022 10:44:57 UTC+02

import numpy as np

from pkg_resources import resource_filename
from sklearn.pipeline import make_pipeline

from bob.bio.base.test.utils import is_library_available
from bob.bio.spear.transformer import PathToAudio, Resample
from bob.pipelines import Sample, wrap


@is_library_available("torchaudio")
def test_path_to_audio():
    """Tries to load the audio data from a file."""
    audio_path = resource_filename("bob.bio.spear.test", "data/sample.wav")
    audio_n_samples = 77760
    audio_sample_rate = 16000

    sample = Sample(data=audio_path)
    transformer = PathToAudio()
    results = transformer.transform([sample])[0]
    assert results.rate == audio_sample_rate, results.rate
    assert isinstance(results.data, np.ndarray)
    assert results.data.shape == (audio_n_samples,), results.data.shape

    assert results.data.dtype == np.float32, results.data.dtype

    # Force a different sample rate
    sample = Sample(data=audio_path)
    transformer = PathToAudio(forced_sr=audio_sample_rate // 2)
    results = transformer.transform([sample])[0]
    assert results.rate == audio_sample_rate // 2, results.rate
    assert isinstance(results.data, np.ndarray)
    assert results.data.shape == (audio_n_samples // 2,), results.data.shape


@is_library_available("torchaudio")
def test_resample():
    """Resample using the transformer."""
    audio_path = resource_filename("bob.bio.spear.test", "data/sample.wav")
    audio_n_samples = 77760
    audio_sample_rate = 16000

    sample = Sample(data=audio_path, channel=None, rate=audio_sample_rate)
    pipeline = make_pipeline(
        PathToAudio(), wrap(["sample"], Resample(audio_sample_rate // 2))
    )
    results = pipeline.transform([sample])[0]
    assert results.data.shape == (audio_n_samples // 2,), results.data.shape
