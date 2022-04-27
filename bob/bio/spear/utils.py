import numpy as np


def normalize_std_array(vector: np.ndarray):
    """Applies a unit mean and variance normalization to an arrayset"""
    return (
        vector
        if vector.std(axis=0) == 0
        else (vector - vector.mean(axis=0)) / vector.std(axis=0)
    )


def smoothing(labels, smoothing_window):
    """Applies a smoothing on VAD"""

    if np.sum(labels) < smoothing_window:
        return labels

    segments = []
    for k in range(1, len(labels) - 1):
        if labels[k] == 0 and labels[k - 1] == 1 and labels[k + 1] == 1:
            labels[k] = 1
    for k in range(1, len(labels) - 1):
        if labels[k] == 1 and labels[k - 1] == 0 and labels[k + 1] == 0:
            labels[k] = 0

    seg = np.array([0, 0, labels[0]])
    for k in range(1, len(labels)):
        if labels[k] != labels[k - 1]:
            seg[1] = k - 1
            segments.append(seg)
            seg = np.array([k, k, labels[k]])
    seg[1] = len(labels) - 1
    segments.append(seg)

    if len(segments) < 2:
        return labels

    curr = segments[0]
    next = segments[1]

    # Look at the first segment. If it's short enough, just change its labels
    if (curr[1] - curr[0] + 1) < smoothing_window and (
        next[1] - next[0] + 1
    ) > smoothing_window:
        if curr[2] == 1:
            labels[curr[0] : (curr[1] + 1)] = 0
            curr[2] = 0
        else:  # curr[2]==0
            labels[curr[0] : (curr[1] + 1)] = 1
            curr[2] = 1

    for k in range(1, len(segments) - 1):
        prev = segments[k - 1]
        curr = segments[k]
        next = segments[k + 1]

        if (
            (curr[1] - curr[0] + 1) < smoothing_window
            and (prev[1] - prev[0] + 1) > smoothing_window
            and (next[1] - next[0] + 1) > smoothing_window
        ):
            if curr[2] == 1:
                labels[curr[0] : (curr[1] + 1)] = 0
                curr[2] = 0
            else:  # curr[2]==0
                labels[curr[0] : (curr[1] + 1)] = 1
                curr[2] = 1

    prev = segments[-2]
    curr = segments[-1]

    if (curr[1] - curr[0] + 1) < smoothing_window and (
        prev[1] - prev[0] + 1
    ) > smoothing_window:
        if curr[2] == 1:
            labels[curr[0] : (curr[1] + 1)] = 0
            curr[2] = 0
        else:  # if curr[2]==0
            labels[curr[0] : (curr[1] + 1)] = 1
            curr[2] = 1

    return labels


def stack_speech_data(data, expected_ndim):
    """Stacks the speech data into a matrix of shape (n_samples, n_features) or
    labels into shape of (n_samples,) if the input data is not like that already

    Parameters
    ----------
    data : array-like
        speech data or labels
    expected_ndim : int
        expected number of dimensions of the data

    Returns
    -------
    stacked_data : array-like
        stacked data if needed
    """
    if expected_ndim not in (1, 2):
        raise ValueError(f"expected_ndim must be 1 or 2 but got {expected_ndim}")

    if expected_ndim == 1:
        stack_function = np.concatenate
    else:
        stack_function = np.vstack

    if data[0].ndim == expected_ndim:
        return stack_function(data)

    return data



# gets sphinx autodoc done right - don't remove it
__all__ = [_ for _ in dir() if not _.startswith("_")]
