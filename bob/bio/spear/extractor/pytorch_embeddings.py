"""Loads pytorch models and extracts embeddings from samples."""


import abc

import numpy as np
import torch

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils import check_array


class PyTorchModel(TransformerMixin, BaseEstimator):
    """
    Base Transformer using pytorch models


    Parameters
    ----------

    checkpoint_path: str
       Path containing the checkpoint

    config:
        Path containing some configuration file (e.g. .json, .prototxt)

    preprocessor:
        A function that will transform the data right before forward. The default transformation is `X/255`

    """

    def __init__(
        self,
        checkpoint_path=None,
        config=None,
        preprocessor=lambda x: x / 255,
        memory_demanding=False,
        device=None,
        **kwargs,
    ):

        super().__init__(**kwargs)
        self.checkpoint_path = checkpoint_path
        self.config = config
        self.model = None
        self.preprocessor = preprocessor
        self.memory_demanding = memory_demanding
        self.device = torch.device(
            device or "cuda" if torch.cuda.is_available() else "cpu"
        )

    def transform(self, X):
        """__call__(image) -> feature

        Extracts the features from the given image.

        Parameters
        ----------

        image : 2D :py:class:`numpy.ndarray` (floats)
        The image to extract the features from.

        Returns
        -------

        feature : 2D or 3D :py:class:`numpy.ndarray` (floats)
        The list of features extracted from the image.
        """
        if self.model is None:
            self._load_model()
        X = check_array(X, allow_nd=True)
        X = torch.Tensor(X)
        with torch.no_grad():
            X = self.preprocessor(X)

        def _transform(X):
            with torch.no_grad():
                return self.model(X.to(self.device)).cpu().detach().numpy()

        if self.memory_demanding:
            features = np.array([_transform(x[None, ...]) for x in X])

            # If we ndim is > than 2. We should stack them all
            # The enroll_features can come from a source where there are `N` samples containing
            # nxd samples
            if features.ndim >= 2:
                features = np.vstack(features)

            return features

        return _transform(X)

    def __getstate__(self):
        # Handling unpicklable objects
        d = self.__dict__.copy()
        d["model"] = None
        return d

    def _more_tags(self):
        return {"requires_fit": False}

    def place_model_on_device(self):
        if self.model is not None:
            self.model.to(self.device)

    @abc.abstractmethod
    def _load_model(self) -> None:
        """Sets ``self.model``."""
