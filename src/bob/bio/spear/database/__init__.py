#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Elie Khoury <Elie.Khoury@idiap.ch>
# Fri Aug 30 11:42:11 CEST 2013
#
# Copyright (C) 2012-2013 Idiap Research Institute, Martigny, Switzerland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Feature extraction tools"""

from .asvspoof import AsvspoofDatabase
from .avspoof import AvspoofDatabase
from .mobio import MobioDatabase
from .nist_sre04to16 import NistSRE04To16Database
from .timit import TimitDatabase
from .voicepa import VoicepaDatabase
from .voxceleb import VoxcelebDatabase
from .voxforge import VoxforgeDatabase


# gets sphinx autodoc done right - don't remove it
def __appropriate__(*args):
    """Says object was actually declared here, and not in the import module.
    Fixing sphinx warnings of not being able to find classes, when path is shortened.
    Parameters:

      *args: An iterable of objects to modify

    Resolves `Sphinx referencing issues
    <https://github.com/sphinx-doc/sphinx/issues/3048>`
    """

    for obj in args:
        obj.__module__ = __name__


__appropriate__(
    AsvspoofDatabase,
    AvspoofDatabase,
    MobioDatabase,
    NistSRE04To16Database,
    TimitDatabase,
    VoicepaDatabase,
    VoxcelebDatabase,
    VoxforgeDatabase,
)
__all__ = [_ for _ in dir() if not _.startswith("_")]
