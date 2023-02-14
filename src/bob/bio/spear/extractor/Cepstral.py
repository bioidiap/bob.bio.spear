#!/usr/bin/env python
# Elie Khoury <Elie.Khoury@idiap.ch>
# Amir Mohammadi <amir.mohammadi@idiap.ch>

"""Cepstral Features for speaker recognition"""

import logging

import numpy

from sklearn.base import BaseEstimator, TransformerMixin

from .. import audio_processing as ap

logger = logging.getLogger(__name__)


class Cepstral(BaseEstimator, TransformerMixin):
    """Extracts the Cepstral features of audio wav data.

    Use a SampleWrapper to use with bob pipelines to pass the `rate` and `annotations`
    attributes to the arguments of `transform`:
    >>> wrap(
    ...     ["sample"],
    ...     Cepstral(),
    ...     transform_extra_arguments=[
    ...         ("sample_rate", "rate"), ("vad_labels", "annotations")
    ...     ]
    ... )
    """

    def __init__(
        self,
        win_length_ms=20,
        win_shift_ms=10,
        n_filters=24,
        dct_norm=False,
        f_min=0.0,
        f_max=4000.0,
        delta_win=2,
        mel_scale=True,
        with_energy=True,
        with_delta=True,
        with_delta_delta=True,
        n_ceps=19,  # 0-->18
        pre_emphasis_coef=0.95,
        features_mask=None,
        normalize_flag=True,
        **kwargs,
    ):
        """Most parameters are passed to `ap.cepstral`.

        Parameters
        ----------
        features_mask: numpy slice
            Indices of features to keep (only applied if VAD annotations are present).
        normalize_flag: bool
            Controls the normalization of the feature vectors after Cepstral.
        """

        super().__init__(**kwargs)
        self.win_length_ms = win_length_ms
        self.win_shift_ms = win_shift_ms
        self.n_filters = n_filters
        self.dct_norm = dct_norm
        self.f_min = f_min
        self.f_max = f_max
        self.delta_win = delta_win
        self.mel_scale = mel_scale
        self.with_energy = with_energy
        self.with_delta = with_delta
        self.with_delta_delta = with_delta_delta
        self.n_ceps = n_ceps
        self.pre_emphasis_coef = pre_emphasis_coef
        self.features_mask = features_mask
        self.normalize_flag = normalize_flag

    def normalize_features(self, params: numpy.ndarray):
        """Returns the features normalized along the columns.

        Parameters
        ----------
        params:
            2D array of feature vectors.
        """

        # if there is only 1 frame, we cannot normalize it
        if len(params) == 1 or (params.std(axis=0) == 0).any():
            return params
        # normalized_vector is mean std normalized version of params per feature dimension
        normalized_vector = (params - params.mean(axis=0)) / params.std(axis=0)
        return normalized_vector

    def transform_one(
        self,
        wav_data: numpy.ndarray,
        sample_rate: float,
        vad_labels: numpy.ndarray,
    ):
        """Computes and returns cepstral features for one given audio signal."""
        logger.debug("Cepstral transform.")

        cepstral_features = ap.cepstral(
            wav_data,
            sample_rate,
            win_length_ms=self.win_length_ms,
            win_shift_ms=self.win_shift_ms,
            n_filters=self.n_filters,
            f_min=self.f_min,
            f_max=self.f_max,
            pre_emphasis_coef=self.pre_emphasis_coef,
            mel_scale=self.mel_scale,
            n_ceps=self.n_ceps,
            delta_win=self.delta_win,
            dct_norm=self.dct_norm,
            with_energy=self.with_energy,
            with_delta=self.with_delta,
            with_delta_delta=self.with_delta_delta,
        )

        if vad_labels is not None:  # Don't apply VAD if labels are not present
            vad_labels = numpy.array(
                vad_labels
            )  # Ensure array, as `list == 1` is `False`
            filtered_features = cepstral_features[vad_labels == 1]
            if self.features_mask is not None:
                filtered_features = filtered_features[:, self.features_mask]
        else:
            filtered_features = cepstral_features

        if self.normalize_flag:
            normalized_features = self.normalize_features(filtered_features)
        else:
            normalized_features = filtered_features

        if normalized_features.shape[0] == 0:
            logger.warning("No speech found for this utterance")
            # But do not keep it empty!!! This avoids errors in next steps
            feature_length = (
                len(self.features_mask) if self.features_mask else 60
            )
            normalized_features = numpy.zeros((1, feature_length))
        return normalized_features

    def transform(
        self,
        wav_data_set: "list[numpy.ndarray]",
        sample_rate: "list[float]",
        vad_labels: "list[numpy.ndarray]",
    ):
        results = []
        for wav_data, rate, annotations in zip(
            wav_data_set, sample_rate, vad_labels
        ):
            results.append(self.transform_one(wav_data, rate, annotations))
        return results

    def fit(self, X, y=None, **fit_params):
        return self

    def _more_tags(self):
        return {
            "requires_fit": False,
            "bob_transform_extra_input": (
                ("sample_rate", "rate"),
                ("vad_labels", "annotations"),
            ),
        }
