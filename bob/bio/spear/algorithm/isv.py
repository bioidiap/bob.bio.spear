#!/usr/bin/env python
# @author: Yannick Dayer <yannick.dayer@idiap.ch>
# @date: Thu 31 Mar 2022 16:49:42 UTC+02

import logging
import pickle
from bob.pipelines import SampleSet

import numpy as np
from sklearn.preprocessing import OrdinalEncoder
from sklearn.base import TransformerMixin, BaseEstimator

from bob.bio.base.pipelines import BioAlgorithm
from bob.learn.em import ISVMachine
from ..utils import stack_speech_data
from .gmm import GMM

logger = logging.getLogger(__name__)


class ISV(ISVMachine, BioAlgorithm):
    """Tool for computing Unified Background Models and Gaussian Mixture Models of the features"""

    def __init__(
        self,
        # ISV training
        r_U,  # U subspace dimension
        em_iterations=10,  # Number of EM iterations for the ISV training
        relevance_factor=4,
        # ISV enrollment
        enroll_iterations=1,  # Number of iterations for the enrollment phase
        random_state=0,
        # parameters of the GMM
        ubm=None,
        ubm_kwargs=None,
        **kwargs,
    ):
        """Initializes the local UBM-GMM tool with the given file selector object"""
        if ubm_kwargs:
            ubm_kwargs["gmm_class"] = GMM

        super().__init__(
            r_U=r_U,
            em_iterations=em_iterations,
            relevance_factor=relevance_factor,
            random_state=random_state,
            ubm=ubm,
            ubm_kwargs=ubm_kwargs,
            **kwargs,
        )
        self.enroll_iterations = enroll_iterations

    def fit(self, X, y):
        """Train Projector (GMM) and Enroller at the same time"""
        # if input is a list (or SampleBatch) of 2 dimensional arrays, stack them
        X = stack_speech_data(X, expected_ndim=2)
        y = stack_speech_data(y, expected_ndim=1)
        # Train the ISV background model
        logger.info("ISV: Training the ISVMachine.")
        super().fit(X, y)
        return self

    def enroll(self, enroll_features):
        """Performs ISV enrollment

        Parameters
        ----------
        enroll_features : list of numpy.ndarray
            The features to be enrolled.
        """
        enroll_features = stack_speech_data(enroll_features, expected_ndim=2)
        return super().enroll(enroll_features)

    def transform(self, X):
        """Passthrough"""
        return X

    @classmethod
    def custom_enrolled_save_fn(cls, data, path):
        pickle.dump(data, open(path, "wb"))

    @classmethod
    def custom_enrolled_load_fn(cls, path):
        return pickle.load(open(path, "rb"))

    def _more_tags(self):
        return {
            "bob_fit_supports_dask_array": True,
            "bob_fit_extra_input": [("y", "reference_id_int")],
            "bob_enrolled_save_fn": self.custom_enrolled_save_fn,
            "bob_enrolled_load_fn": self.custom_enrolled_load_fn,
            "requires_fit": True,
            "stateless": False,
        }


class ReferenceIdEncoder(OrdinalEncoder):
    # Default values of init args are different from the base class
    def __init__(
        self,
        *,
        categories="auto",
        dtype=int,
        handle_unknown="use_encoded_value",
        unknown_value=-1,
        **kwargs,
    ):
        super().__init__(
            categories=categories,
            dtype=dtype,
            handle_unknown=handle_unknown,
            unknown_value=unknown_value,
            **kwargs,
        )

    def fit(self, X, y=None):
        # X is a SampleBatch or list of reference_id strings
        # we want a 2d array of shape (N, 1)
        X = np.asarray(X).reshape((-1, 1))
        return super().fit(X)

    def transform(self, X):
        X = np.asarray(X).reshape((-1, 1))
        # we output a flat array instead
        return super().transform(X).flatten()

    def _more_tags(self):
        return {
            "bob_input": "reference_id",
            "bob_output": "reference_id_int",
            "bob_features_save_fn": ISV.custom_enrolled_save_fn,
            "bob_features_load_fn": ISV.custom_enrolled_load_fn,
        }


class LabelRepeater(TransformerMixin, BaseEstimator):
    """Repeats the labels of the samples to be as big as each data sample."""

    def __init__(self, label_attr, data_attr="data", **kwargs):
        super().__init__(**kwargs)
        self.label_attr = label_attr
        self.data_attr = data_attr

    def transform(self, labels, data):
        data_lengths = [len(d) for d in data]
        new_labels = []
        for label, repeat in zip(labels, data_lengths):
            new_labels.append(np.repeat(label, repeat))
        return new_labels

    def fit(self, X, y=None):
        return self

    def _more_tags(self):
        return {
            "bob_input": self.label_attr,
            "bob_transform_extra_input": [("data", self.data_attr)],
            "bob_output": self.label_attr,
            "requires_fit": False,
            "stateless": False,
        }
