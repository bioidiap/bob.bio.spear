#!/usr/bin/env python
# @author: Yannick Dayer <yannick.dayer@idiap.ch>
# @date: Thu 31 Mar 2022 16:49:42 UTC+02
# Amir Mohammadi <amir.mohammadi@idiap.ch>

import logging
import pickle

from bob.bio.base.pipelines import BioAlgorithm
from bob.learn.em import ISVMachine

logger = logging.getLogger(__name__)


class ISV(ISVMachine, BioAlgorithm):
    """Tool for computing Unified Background Models and Gaussian Mixture Models of the features"""

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
            "bob_fit_supports_dask_bag": True,
            "bob_fit_extra_input": [("y", "reference_id_int")],
            "bob_enrolled_save_fn": self.custom_enrolled_save_fn,
            "bob_enrolled_load_fn": self.custom_enrolled_load_fn,
            "bob_checkpoint_features": False,
        }
