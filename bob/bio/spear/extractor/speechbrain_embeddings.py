import numpy as np
import torch

from sklearn.base import BaseEstimator
from speechbrain.pretrained import EncoderClassifier


class SpeechbrainEmbeddings(BaseEstimator):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def fit(self, X, y=None):
        return self

    def transform_one(self, encoder, audio_track):
        return encoder.encode_batch(
            torch.from_numpy(audio_track),
            normalize=True,
        ).numpy()

    def transform(self, audio_tracks, y=None):
        encoder = EncoderClassifier.from_hparams(
            source="speechbrain/spkrec-ecapa-voxceleb",
            savedir="pretrained_models/spkrec-ecapa-voxceleb",
        )
        lengths = [len(m) for m in audio_tracks]

        audio_stack = np.vstack(
            [
                np.pad(m, (0, max(lengths) - len(m)), "constant")
                for m in audio_tracks
            ]
        )
        relative_lengths = [length / max(lengths) for length in lengths]

        embeddings = encoder.encode_batch(
            torch.from_numpy(audio_stack),
            torch.tensor(relative_lengths),
            normalize=True,
        )

        return embeddings.numpy()
