#!/usr/bin/env python
# @author: Yannick Dayer <yannick.dayer@idiap.ch>
# @date: Thu 31 Mar 2022 16:49:42 UTC+02

import logging

import numpy
import numpy as np

from h5py import File as HDF5File
from sklearn.base import BaseEstimator

from bob.bio.base.pipelines.vanilla_biometrics import BioAlgorithm
from bob.bio.gmm.algorithm import GMM
from bob.learn.em import GMMMachine
from bob.learn.em import GMMStats
from bob.learn.em import ISVMachine

logger = logging.getLogger(__name__)


class ISV(BioAlgorithm, BaseEstimator):
    """Tool for computing Unified Background Models and Gaussian Mixture Models of the features"""

    def __init__(
        self,
        # ISV training
        subspace_dimension_of_u,  # U subspace dimension
        isv_training_iterations=10,  # Number of EM iterations for the ISV training
        # ISV enrollment
        isv_enroll_iterations=1,  # Number of iterations for the enrollment phase
        # parameters of the GMM
        **kwargs
    ):
        """Initializes the local UBM-GMM tool with the given file selector object"""

        self.subspace_dimension_of_u = subspace_dimension_of_u
        self.isv_training_iterations = isv_training_iterations
        self.isv_enroll_iterations = isv_enroll_iterations
        self.ubm = None

        self.gmm_algorithm = GMM(**kwargs)

    def train_isv(self, data):
        """Train the ISV model given a dataset"""
        logger.info("  -> Training ISV enroller")
        # self.isvbase = ISVBase(self.ubm, self.subspace_dimension_of_u)
        # Train the ISV model
        self.isv_machine.fit(data)

    def fit(self, train_features, reference_ids):
        """Train Projector and Enroller at the same time"""

        # Train the gmm
        self.gmm_algorithm.fit(np.vstack(train_features))
        self.ubm = self.gmm_algorithm.ubm

        # Group the training features by reference id
        grouped_features = {}
        for ref_id, features in zip(reference_ids, train_features):
            ref_id = ref_id[0][0].compute()
            if ref_id not in grouped_features:
                grouped_features[ref_id] = []
            grouped_features[ref_id].append(features)

        # project training data
        logger.info("  -> Projecting training data")
        data = [
            [self.gmm_algorithm.project(feature) for feature in client]
            for client in grouped_features.values()
        ]

        # train ISV
        self.train_isv(data)

    def load_isv(self, isv_file):
        # hdf5file = HDF5File(isv_file, "r")
        # self.isvbase = bob.learn.em.ISVBase(hdf5file)
        # add UBM model from base class
        self.isvbase.ubm = self.ubm

    def load_projector(self, projector_file):
        """Load the GMM and the ISV model from the same HDF5 file"""
        hdf5file = HDF5File(projector_file, "r")

        # Load Projector
        hdf5file.cd("/Projector")
        self.load_ubm(hdf5file)

        # Load Enroller
        hdf5file.cd("/Enroller")
        self.load_isv(hdf5file)

    #######################################################
    #                ISV training                         #
    def project_isv(self, projected_ubm):
        projected_isv = numpy.ndarray(
            shape=(self.ubm.shape[0] * self.ubm.shape[1],), dtype=numpy.float64
        )
        model = ISVMachine(self.isvbase)
        model.estimate_ux(projected_ubm, projected_isv)
        return projected_isv

    def project(self, feature):
        """Computes GMM statistics against a UBM, then corresponding Ux vector"""
        self._check_feature(feature)
        projected_ubm = GMM.project(self, feature)
        projected_isv = self.project_isv(projected_ubm)
        return [projected_ubm, projected_isv]

    #######################################################
    #                 ISV model enroll                    #

    def write_feature(self, data, feature_file):
        gmmstats = data[0]
        Ux = data[1]
        hdf5file = (
            HDF5File(feature_file, "w")
            if isinstance(feature_file, str)
            else feature_file
        )
        hdf5file.create_group("gmmstats")
        hdf5file.cd("gmmstats")
        gmmstats.save(hdf5file)
        hdf5file.cd("..")
        hdf5file.set("Ux", Ux)

    def read_feature(self, feature_file):
        """Read the type of features that we require, namely GMMStats"""
        hdf5file = HDF5File(feature_file, "r")
        hdf5file.cd("gmmstats")
        gmmstats = GMMStats(hdf5file)
        hdf5file.cd("..")
        Ux = hdf5file.read("Ux")
        return [gmmstats, Ux]

    def _check_projected(self, probe):
        """Checks that the probe is of the desired type"""
        assert isinstance(probe, (tuple, list))
        assert len(probe) == 2
        assert isinstance(probe[0], GMMStats)
        assert (
            isinstance(probe[1], numpy.ndarray)
            and probe[1].ndim == 1
            and probe[1].dtype == numpy.float64
        )

    def enroll(self, enroll_features):
        """Performs ISV enrollment"""
        for feature in enroll_features:
            self._check_projected(feature)
        machine = ISVMachine(self.isvbase)
        self.isv_trainer.enroll(
            machine, [f[0] for f in enroll_features], self.isv_enroll_iterations
        )
        # return the resulting gmm
        return machine

    ######################################################
    #                Feature comparison                  #
    def read_model(self, model_file):
        """Reads the ISV Machine that holds the model"""
        machine = ISVMachine(HDF5File(model_file, "r"))
        machine.isv_base = self.isvbase
        return machine

    def score(self, model, probe):
        """Computes the score for the given model and the given probe."""
        assert isinstance(model, ISVMachine)
        self._check_projected(probe)

        gmmstats = probe[0]
        Ux = probe[1]
        return model.forward_ux(gmmstats, Ux)

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
    #         projected_isv_acc = numpy.ndarray(
    #             shape=(self.ubm.shape[0] * self.ubm.shape[1],), dtype=numpy.float64
    #         )
    #         model.estimate_ux(gmmstats_acc, projected_isv_acc)
    #         return model.forward_ux(gmmstats_acc, projected_isv_acc)

    @classmethod
    def custom_enrolled_save_fn(cls, data, path):
        data.save(path)

    def custom_enrolled_load_fn(self, path):
        return GMMMachine.from_hdf5(path, ubm=self.ubm)

    def _more_tags(self):
        return {
            "bob_fit_supports_dask_array": True,
            "bob_fit_expects_samplesets": True,
            "bob_fit_extra_input": [("reference_ids", "reference_id")],
            "bob_enrolled_save_fn": self.custom_enrolled_save_fn,
            "bob_enrolled_load_fn": self.custom_enrolled_load_fn,
            "requires_fit": True,
            "stateless": False,
        }
