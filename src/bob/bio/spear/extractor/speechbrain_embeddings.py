import numpy as np
import torch

from sklearn.base import BaseEstimator


class SpeechbrainEmbeddings(BaseEstimator):
    def __init__(self, **kwargs) -> None:
        # later on we will add source and savedir as input parameters to allow
        # loading of different models
        super().__init__(**kwargs)

        # set model to None for load_model call
        self.model = None
        # ensure the files are downloaded before dask execution
        self.load_model()
        # only load models when they are used. (Prevents model transfer over the network)
        self.model = None

    def load_model(self):
        if self.model is not None:
            return
        from speechbrain.pretrained import EncoderClassifier

        self.model = EncoderClassifier.from_hparams(
            source="speechbrain/spkrec-ecapa-voxceleb",
            savedir="pretrained_models/spkrec-ecapa-voxceleb",
        )

    def fit(self, X, y=None):
        return self

    def transform_one(self, audio_track):
        return self.model.encode_batch(
            torch.from_numpy(audio_track),
            normalize=True,
        ).numpy()

    def transform(self, audio_tracks, y=None):
        # actual load of the model (on the workers)
        self.load_model()
        embeddings = [
            self.transform_one(audio_track) for audio_track in audio_tracks
        ]

        return np.vstack(embeddings)

    def __getstate__(self):
        # Handling unpicklable objects
        d = self.__dict__.copy()
        d["model"] = None
        return d

    def _more_tags(self):
        return {"requires_fit": False}
