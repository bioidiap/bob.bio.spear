import logging

import numpy as np
import torch

# Download pretrained SpeakerRecognition from SpeechBrain
from speechbrain.pretrained import SpeakerRecognition

from bob.bio.base.pipelines import BioAlgorithm

logger = logging.getLogger(__name__)


class SpeechBrainInterface(BioAlgorithm):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.verification = SpeakerRecognition.from_hparams(
            source="speechbrain/spkrec-ecapa-voxceleb",
            savedir="pretrained_models/spkrec-ecapa-voxceleb",
        )

    def enroll(self, data):
        return data  # Defines the model as the data itself (used during the scoring)

    def score(self, model, data):
        # Compute the score on each audio file of the model
        scores = [
            self.verification.verify_batch(
                torch.from_numpy(m),
                torch.from_numpy(data),
            )[
                0
            ]  # Retrieves the score, discards the decision
            for m in model  # Scores against each sample of model
        ]
        scores = np.array(scores, dtype=float)

        # Reduce to one score for that probe on this model
        return [scores.mean()]
