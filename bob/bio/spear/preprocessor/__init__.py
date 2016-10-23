from .Base import Base
from .Energy_2Gauss import Energy_2Gauss
from .Energy_Thr import Energy_Thr
from .Mod_4Hz import Mod_4Hz
from .External import External

# gets sphinx autodoc done right - don't remove it
def __appropriate__(*args):
  """Says object was actually declared here, and not in the import module.
  Fixing sphinx warnings of not being able to find classes, when path is shortened.
  Parameters:

    *args: An iterable of objects to modify

  Resolves `Sphinx referencing issues
  <https://github.com/sphinx-doc/sphinx/issues/3048>`
  """

  for obj in args: obj.__module__ = __name__

__appropriate__(
    Base,
    Energy_2Gauss,
    Energy_Thr,
    Mod_4Hz,
    External,
    )
__all__ = [_ for _ in dir() if not _.startswith('_')]
