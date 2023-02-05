#!/usr/bin/env python
# @author: Yannick Dayer <yannick.dayer@idiap.ch>
# @date: Wed 16 Jun 2021 17:20:16 UTC+02

"""VoxForge CSV database interface default configuration

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

Feed this file (also defined as a ``voxforge`` resource) to ``bob bio pipelines`` as
configuration::

    $ bob bio pipeline simple voxforge <pipeline_name> -vv
"""

from bob.bio.spear.database import VoxforgeDatabase

default_protocol = "Default"

if "protocol" not in locals():
    protocol = default_protocol

database = VoxforgeDatabase(protocol=protocol)
