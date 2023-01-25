from typing import Any

import numpy as np

from sklearn.base import BaseEstimator
from speechbrain.processing.PLDA_LDA import PLDA as SpeechbrainPLDA
from speechbrain.processing.PLDA_LDA import (
    Ndx,
    StatObject_SB,
    fast_PLDA_scoring,
)

from bob.bio.base.pipelines import BioAlgorithm


class PLDA(BioAlgorithm, BaseEstimator):
    def __init__(self, rank_f: int = 5, **kwargs) -> None:
        self.rank_f = rank_f
        super().__init__(kwargs)
        self.plda_backend = SpeechbrainPLDA(rank_f=self.rank_f)

    def fit(self, X, y=None, **kwargs):
        """Trains the PLDA."""
        id_count = {id: 0 for id in set(y)}
        seg = []
        for ref_id in y:
            seg.append(f"{ref_id}_{id_count[ref_id]}")
            id_count[ref_id] += 1
        stat0 = np.ones(shape=(len(X), 1))
        starts = np.array([None] * len(X))
        stops = np.array([None] * len(X))
        stats = StatObject_SB(
            modelset=np.array(y),
            segset=np.array(seg),
            start=starts,
            stop=stops,
            stat0=stat0,
            stat1=np.array(X),
        )
        self.plda_backend.plda(stats)
        return self

    def transform(self, X):
        """Passthrough"""
        return X

    def create_templates(
        self, list_of_feature_sets: list[Any], enroll: bool = False
    ) -> list[Any]:
        templates = []
        for features in list_of_feature_sets:
            # ids = np.array([f.reference_id for s in features for f in s])
            if enroll:
                ids = np.array(["m"] * len(features))
            else:
                ids = np.array(["t"] * len(features))
            stat0 = np.ones(shape=(ids.shape[0], 1))
            templates.append(
                StatObject_SB(
                    modelset=ids,
                    segset=ids,
                    stat0=stat0,
                    stat1=np.array(features),
                )
            )

        return templates

    def compare(self, enroll_templates, probe_templates):
        # TODO for in enrolls; for in probes?
        return fast_PLDA_scoring(
            enroll_templates,
            probe_templates,
            Ndx(enroll_templates, probe_templates),
            self.plda_backend.mean,
            self.plda_backend.F,
            self.plda_backend.Sigma,
        )

    def _more_tags(self):
        return {
            "requires_fit": True,
            "bob_fit_extra_input": [("y", "reference_id")],
            "bob_enrolled_save_fn": self.custom_enrolled_save_fn,  # TODO
            "bob_enrolled_load_fn": self.custom_enrolled_load_fn,
        }
