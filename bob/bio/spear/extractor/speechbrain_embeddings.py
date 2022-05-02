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
        embeddings = [
            self.transform_one(encoder, audio_track) for audio_track in audio_tracks
        ]

        return np.vstack(embeddings)
