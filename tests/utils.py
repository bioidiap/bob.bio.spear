from functools import wraps
from importlib import import_module
from unittest import SkipTest


def is_library_available(library):
    """Decorator to check if a library is present, before running the test"""

    def _is_library_available(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            try:
                import_module(library)
            except ImportError as e:
                # unittest.SkipTest is compatible with both nose and pytest
                raise SkipTest(
                    f"Skipping test since `{library}` is not available: {e}"
                ) from e
            return function(*args, **kwargs)

        return wrapper

    return _is_library_available
