#!/usr/bin/env python
# @author: Yannick Dayer <yannick.dayer@idiap.ch>
# @date: Thu 31 Mar 2022 16:49:42 UTC+02

import logging
import pickle

import numpy as np
from sklearn.base import BaseEstimator
from sklearn.preprocessing import OrdinalEncoder

from bob.bio.base.pipelines import BioAlgorithm
from bob.bio.gmm.algorithm import GMM
from bob.learn.em import GMMStats, ISVMachine

logger = logging.getLogger(__name__)


class ISV(BioAlgorithm, BaseEstimator):
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

        # Train the gmm
        logger.info("ISV: Training the GMM UBM.")
        self.gmm_algorithm.fit(X)

        # Project training data using the GMM UBM
        logger.info("ISV: Projecting training data on UBM with the GMM.")
        ubm_projected_features = [self.gmm_algorithm.project(f) for f in X]

        # Create the ISV machine based on the GMM UBM
        self.isv_machine = ISVMachine(
            self.gmm_algorithm.ubm,
            r_U=self.subspace_dimension_of_u,
            em_iterations=self.isv_training_iterations,
            relevance_factor=self.isv_relevance_factor,
            seed=self.rng,
        )

        # Train the ISV background model
        logger.info("ISV: Training the ISVMachine with the projected data.")
        self.isv_machine.fit(ubm_projected_features, y)
        return self

    #######################################################
    #                ISV training                         #
    def project_isv(self, projected_ubm: GMMStats):
        return self.isv_machine.estimate_ux(projected_ubm)

    def project(self, feature):
        """Computes GMM statistics against a UBM, then corresponding Ux vector"""
        self.gmm_algorithm._check_feature(feature)
        # Project the feature once on GMM
        projected_ubm = self.gmm_algorithm.project(feature)
        # Feed the projected feature to the ISV projector
        projected_isv = self.project_isv(projected_ubm)
        return [projected_ubm, projected_isv]

    #######################################################
    #                 ISV model enroll                    #

    def _check_projected(self, probe):
        """Checks that the probe is of the desired type"""
        assert isinstance(probe, (tuple, list))
        assert len(probe) == 2
        assert isinstance(probe[0], GMMStats)
        assert (
            isinstance(probe[1], np.ndarray)
            and probe[1].ndim == 1
            and probe[1].dtype == np.float64
        )

    def enroll(self, enroll_features):
        """Performs ISV enrollment

        Parameters
        ----------
        enroll_features : list of numpy.ndarray
            The features to be enrolled.
        """
        projected_features = [self.project(e_f) for e_f in enroll_features]
        for feature in projected_features:
            self._check_projected(feature)
        return self.isv_machine.enroll(
            [f[0] for f in projected_features], self.isv_enroll_iterations
        )

    ######################################################
    #                Feature comparison                  #

    def score(self, model, probe):
        """Computes the score for the given model and the given probe."""
        # assert isinstance(model, ISVMachine), type(model)
        # projected_probe = self.project(probe)
        # self._check_projected(projected_probe)

        # gmm_stats = projected_probe[0]
        # Ux = projected_probe[1]
        projected_probe = self.gmm_algorithm.project(probe)
        return self.isv_machine.score(model, projected_probe)

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
