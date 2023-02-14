#!/usr/bin/env python
# @author: Yannick Dayer <yannick.dayer@idiap.ch>
# @date: Mon 13 Feb 2022 16:34:27 UTC+01

"""Mini Subset of VoxForge CSV database interface default configuration

VoxForge is an open speech dataset that was set up to collect transcribed speech for
use with Free and Open Source Speech Recognition Engines. (http://www.voxforge.org/)

This database interface uses a subset of the full dataset used for speaker recognition.
The list of data files in the subset is defined by a CSV file for each protocol. Use
the ``bob db voxforge-download`` command to retrieve those data files if needed, and
set the config with the correct path with ``bob config set bob.db.voxforge.directory``.

The protocol definition files are available at
https://www.idiap.ch/software/bob/data/bob/bob.bio.spear/ and downloaded automatically
(by default into ``bob_data_folder`` which is configurable with ``bob config``).


Usage
-----

Feed this file (also defined as a ``mini-voxforge`` resource) to ``bob bio pipelines``
as configuration::

    $ bob bio pipeline simple mini-voxforge <pipeline_name> -vv
"""

from bob.bio.spear.database import VoxforgeDatabase

database = VoxforgeDatabase(protocol="Mini")
