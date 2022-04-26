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

    def enroll(self, model_samples):

        m_lengths = [len(m) for m in model_samples]

        model_stack = np.vstack(
            [np.pad(m, (0, max(m_lengths) - len(m)), "constant") for m in model_samples]
        )
        relative_m_lengths = [length / max(m_lengths) for length in m_lengths]

        embeddings = self.verification.encode_batch(
            torch.from_numpy(model_stack),
            torch.tensor(relative_m_lengths),
            normalize=True,
        )

        return embeddings  # Embeddings corresponding to one model

    def score(self, model_embeddings, probe_sample):

        data_embedding = self.verification.encode_batch(
            torch.from_numpy(probe_sample), normalize=True
        )

        score = self.verification.similarity(model_embeddings, data_embedding)

        return [np.array(score, dtype=float).mean()]
