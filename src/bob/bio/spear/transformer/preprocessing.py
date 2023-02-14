import numpy as np

from sklearn.preprocessing import OrdinalEncoder


class ReferenceIdEncoder(OrdinalEncoder):
    # Default values of init args are different from the base class
    def __init__(
        self,
        *,
        categories="auto",
        dtype=int,
        handle_unknown="use_encoded_value",
        unknown_value=-1,
        **kwargs,
    ):
        super().__init__(
            categories=categories,
            dtype=dtype,
            handle_unknown=handle_unknown,
            unknown_value=unknown_value,
            **kwargs,
        )

    def fit(self, X, y=None):
        # X is a SampleBatch or list of template_id strings
        # we want a 2d array of shape (N, 1)
        X = np.asarray(X).reshape((-1, 1))
        return super().fit(X)

    def transform(self, X):
        X = np.asarray(X).reshape((-1, 1))
        # we output a flat array instead
        return super().transform(X).flatten()

    def _more_tags(self):
        return {
            "bob_input": "subject_id",
            "bob_output": "subject_id_int",
        }
