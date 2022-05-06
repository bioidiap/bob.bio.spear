#!/usr/bin/env python
# Yannick Dayer <yannick.dayer@idiap.ch>
# Thu 14 Apr 2022 11:31:46 UTC+02

"""Transformer definition for audio data augmentation.

Notably for the NIST-SRE database.
"""


import librosa
import numpy as np

from scipy.signal import convolve
from sklearn.base import BaseEstimator


def reverberate(audio, audio_rate, rir_file):
    """Reverberates the input audio signal according to a Room Impulse Response (rir).

    Parameters
    ----------
    audio : ndarray, shape (n_samples,)
        The audio signal to reverberate.
    rir_file : str
        The file containing the impulse response.
    audio_rate : int
        The sampling rate of the input audio signal. Output will be resampled at this
        rate.

    Returns
    -------
    reverberated : ndarray, shape (n_samples,)
        The reverberated signal.
    """
    # Load the impulse response and resample it to the input audio rate
    rir, _ = librosa.load(rir_file, sr=audio_rate)

    # Compute the reverberation
    reverberated = convolve(audio, rir, mode="full")

    # Copy Kaldi's behavior: output is shifted by the peak offset of the impulse
    #   response and truncated to the length of the input signal.
    peak_offset = np.argmax(rir)
    reverberated = reverberated[peak_offset : peak_offset + len(audio)]

    # Scale the output to have the same energy as the input
    power_before = np.sum(audio**2) / len(audio)
    power_after = np.sum(reverberated**2) / len(reverberated)
    reverberated *= np.sqrt(power_before / power_after)

    # Return the reverberated signal
    return reverberated


def add_noise(
    audio: np.ndarray,
    audio_rate: int,
    noise_files: list,
    noise_offsets: list,
    noise_durations: list,
    noise_levels_db: list,
    normalize: bool = True,
) -> np.ndarray:
    """Adds noise to the input audio signal.

    Parameters
    ----------
    audio: shape (n_samples,)
        The audio signal to reverberate.
    noise_files
        The list of noise files to use.
    noise_offsets
        The list of offsets (in seconds) to use for each noise file.
    noise_durations
        The list of durations (in seconds) to use for each noise file. If the file is
        too short, the audio noise will be repeated.
    noise_levels_db
        The list of noise levels in dB to use for each noise file.
    normalize
        Whether to normalize the output signal to have the same energy as the input.

    Returns
    -------
    noise_added: shape (n_samples,)
        The noise added signal.
    """

    power_before = np.sum(audio**2) / len(audio)

    # Add noises to the signal
    for noise_file, noise_offset, noise_duration, noise_level_db in zip(
        noise_files, noise_offsets, noise_durations, noise_levels_db
    ):

        # Convert times to sample counts
        offset_samples = int(noise_offset * audio_rate)
        duration_samples = int(noise_duration * audio_rate)

        # Ignore this noise if offset is greater than the length of the input
        if offset_samples >= len(audio):
            continue
        # Change the noise duration to fit in the input
        if offset_samples + duration_samples > len(audio):
            duration_samples = len(audio) - offset_samples

        # Load the noise file and resample to match the input audio rate
        noise, _ = librosa.load(
            noise_file, sr=audio_rate, mono=True, res_type="soxr_hq"
        )

        # Repeat or crop the noise to match the duration of the signal
        if len(noise) < duration_samples:
            noise = np.pad(
                noise, (0, duration_samples - len(noise)), mode="wrap"
            )
        else:
            noise = noise[:duration_samples]

        # Scale the noise using the provided SNR
        audio_power = np.sum(audio**2) / len(audio)
        noise_power = np.sum(noise**2) / len(noise)
        scale = np.sqrt(
            10 ** (-noise_level_db / 10) * audio_power / noise_power
        )
        audio[offset_samples : offset_samples + duration_samples] += (
            scale * noise
        )

    # Normalize the audio
    if normalize:
        power_after = np.sum(audio**2) / len(audio)
        audio *= np.sqrt(power_before / power_after)

    # Original Kaldi commands saves with int16 format (effectively truncating).
    audio = np.trunc(audio * 32768) / 32768

    # Return the signal with added noises
    return audio


class Augmentation(BaseEstimator):
    """Transformer for audio data augmentation.

    Requires wrapping with a :py:class:`bob.pipelines.SampleWrapper`.

    Samples must contain an ``augmentation`` metadata.
    """

    def __init__(self, **kwargs):
        """Initialize the transformer.

        Parameters
        ----------
        **kwargs
            Keyword arguments.
        """
        super(Augmentation, self).__init__(**kwargs)

    def fit(self, X, y=None):
        return self

    def transform(
        self,
        X,
        sample_rate: "list[int]",
        rir_file: "list[str]",
        noise_files: "list[list[str]]",
        noise_offsets: "list[list[float]]",
        noise_durations: "list[list[float]]",
        noise_levels_db: "list[list[float]]",
    ):
        """Transform the data.

        Parameters
        ----------
        X : numpy.ndarray
            The data to transform.

        Returns
        -------
        numpy.ndarray
            The transformed data.
        """
        output = []
        for x, sr, rir, n_files, n_offsets, n_durations, n_levels_db in zip(
            X,
            sample_rate,
            rir_file,
            noise_files,
            noise_offsets,
            noise_durations,
            noise_levels_db,
        ):
            # Samples can either have a reverberation or a noise added
            if rir is not None:
                res = reverberate(x, sr, rir)
            elif len(n_files) > 0:
                res = add_noise(
                    x, sr, n_files, n_offsets, n_durations, n_levels_db
                )
            else:
                res = x

            output.append(res)
        return output

    def _more_tags(self):
        return {
            "requires_fit": False,
            "stateless": True,
            "bob_transform_extra_input": [
                ("sample_rate", "rate"),
                ("rir_file", "rir_file"),
                ("noise_files", "noise_files"),
                ("noise_offsets", "noise_offsets"),
                ("noise_durations", "noise_durations"),
                ("noise_levels_db", "noise_levels_db"),
            ],
        }
