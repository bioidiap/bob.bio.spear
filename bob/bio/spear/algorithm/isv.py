#!/usr/bin/env python
# @author: Yannick Dayer <yannick.dayer@idiap.ch>
# @date: Thu 31 Mar 2022 16:49:42 UTC+02

import logging
import pickle
from bob.pipelines import SampleSet

import numpy as np
from sklearn.base import TransformerMixin
from sklearn.preprocessing import OrdinalEncoder, FunctionTransformer

from bob.bio.base.pipelines import BioAlgorithm
from bob.bio.spear.algorithm import GMM
from bob.learn.em import GMMStats, ISVMachine

logger = logging.getLogger(__name__)


class ISV(BioAlgorithm, TransformerMixin):
    """Tool for computing Unified Background Models and Gaussian Mixture Models of the features"""

    def __init__(
        self,
        # ISV training
        subspace_dimension_of_u,  # U subspace dimension
        isv_training_iterations=10,  # Number of EM iterations for the ISV training
        isv_relevance_factor=4,
        # ISV enrollment
        isv_enroll_iterations=1,  # Number of iterations for the enrollment phase
        rng=0,
        # parameters of the GMM
        **kwargs,
    ):
        """Initializes the local UBM-GMM tool with the given file selector object"""

        self.subspace_dimension_of_u = subspace_dimension_of_u
        self.isv_training_iterations = isv_training_iterations
        self.isv_enroll_iterations = isv_enroll_iterations
        self.isv_relevance_factor = isv_relevance_factor
        self.rng = rng

        self.gmm_algorithm = GMM(init_seed=rng, **kwargs)
        self.isv_machine = None

        super(ISV, self).__init__()

    def fit(self, X, y):
        """Train Projector (GMM) and Enroller at the same time"""
        # if input is a list (or SampleBatch) of 2 dimensional arrays, stack them
        if X[0].ndim == 2:
            X = np.vstack(X)
            y = np.concatenate(y, axis=0)

        # Create the ISV machine based on the GMM UBM
        self.isv_machine = ISVMachine(
            r_U=self.subspace_dimension_of_u,
            em_iterations=self.isv_training_iterations,
            relevance_factor=self.isv_relevance_factor,
            seed=self.rng,
            ubm=self.gmm_algorithm.ubm,
        )

        # Train the ISV background model
        logger.info("ISV: Training the ISVMachine with the projected data.")
        self.isv_machine.fit(X, y)
        return self

    def enroll(self, enroll_features):
        """Performs ISV enrollment

        Parameters
        ----------
        enroll_features : list of numpy.ndarray
            The features to be enrolled.
        """
        if enroll_features[0].ndim == 2:
            enroll_features = np.vstack(enroll_features)

        return self.isv_machine.enroll(
            enroll_features, self.isv_enroll_iterations
        )

    ######################################################
    #                Feature comparison                  #

    def score(self, model, probe):
        """Computes the score for the given model and the given probe."""
        return self.isv_machine.score(model, probe)

    # def score_for_multiple_probes(self, model, probes):
    #     """This function computes the score between the given model and several given probe files."""
    #     assert isinstance(model, bob.learn.em.ISVMachine)
    #     [self._check_projected(probe) for probe in probes]
    #     if self.probe_fusion_function is not None:
    #         # When a multiple probe fusion function is selected, use it
    #         return Algorithm.score_for_multiple_probes(self, model, probes)
    #     else:
    #         # Otherwise: compute joint likelihood of all probe features
    #         # create GMM statistics from first probe statistics
    #         #      import pdb; pdb.set_trace()
    #         gmmstats_acc = bob.learn.em.GMMStats(probes[0][0])
    #         #      gmmstats_acc = probes[0][0]
    #         # add all other probe statistics
    #         for i in range(1, len(probes)):
    #             gmmstats_acc += probes[i][0]
    #         # compute ISV score with the accumulated statistics
    #         projected_isv_acc = np.ndarray(
    #             shape=(self.ubm.shape[0] * self.ubm.shape[1],), dtype=np.float64
    #         )
    #         model.estimate_ux(gmmstats_acc, projected_isv_acc)
    #         return model.forward_ux(gmmstats_acc, projected_isv_acc)

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


def label_repeater(samples, label_attr, data_attr="data"):
    """
    This function repeats the labels of the samples to be as big as each data sample.
    """
    if isinstance(samples[0], SampleSet):
        return [
                SampleSet(
                    label_repeater(sset.samples, data_attr, label_attr),
                    parent=sset,
                )
                for sset in samples
            ]
    # we want to repeat labels to be as big as each data sample
    labels = [getattr(sample, label_attr) for sample in samples]
    data_lengths = [len(getattr(sample, data_attr)) for sample in samples]
    for sample, label, repeat in zip(samples, labels, data_lengths):
        setattr(sample, label_attr, np.repeat(label, repeat))
    return samples


def LabelRepeater(label_attr, data_attr="data"):
    return FunctionTransformer(
        func=label_repeater,
        validate=False,
        kw_args={"data_attr": data_attr, "label_attr": label_attr},
    )
