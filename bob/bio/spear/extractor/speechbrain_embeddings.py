import numpy as np
import torch
from sklearn.base import BaseEstimator
from speechbrain.pretrained import EncoderClassifier


class SpeechbrainEmbeddings(BaseEstimator):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def fit(self, X, y=None):
        return self

    def transform(self, audio_tracks, y=None):

        audio_lengths = [len(a) for a in audio_tracks]

        audio_stack = np.vstack(
            [
                np.pad(a, (0, max(audio_lengths) - len(a)), "constant")
                for a in audio_tracks
            ]
        )
        relative_lengths = [length / max(audio_lengths) for length in audio_lengths]

        verification = EncoderClassifier.from_hparams(
            source="speechbrain/spkrec-ecapa-voxceleb",
            savedir="pretrained_models/spkrec-ecapa-voxceleb",
        )

        embeddings = verification.encode_batch(
            torch.from_numpy(audio_stack),
            torch.tensor(relative_lengths),
            normalize=True,
        )

        return np.array(
            embeddings, dtype=float
        )  # Embeddings corresponding to one model
