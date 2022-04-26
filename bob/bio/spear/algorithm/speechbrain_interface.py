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

        m_length = [len(m) for m in model]

        model_stack = np.vstack(
            [np.pad(m, (0, max(m_length) - len(m)), "constant") for m in model]
        )
        relative_m_length = [length / (max(m_length)) for length in m_length]
        scores, _ = self.verification.verify_batch(
            torch.from_numpy(model_stack),
            torch.from_numpy(data),
            torch.tensor(relative_m_length),
        )
        scores = np.array(scores, dtype=float)

        # Reduce to one score for that probe on this model
        return [scores.mean()]

        # # Compute the score on each audio file of the model
        # scores = [
        #     self.verification.verify_batch(
        #         torch.from_numpy(m),
        #         torch.from_numpy(data),
        #     )[
        #         0
        #     ]  # Retrieves the score, discards the decision
        #     for m in model  # Scores against each sample of model
        # ]
        # scores = np.array(scores, dtype=float)

        # # Reduce to one score for that probe on this model
        # return [scores.mean()]
