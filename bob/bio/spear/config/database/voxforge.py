#!/usr/bin/env python
# Yannick Dayer <yannick.dayer@idiap.ch>
# Wed 16 Jun 2021 17:20:16 UTC+02

"""VoxForge CSV database interface default configuration

VoxForge is an open speech dataset that was set up to collect transcribed speech for
use with Free and Open Source Speech Recognition Engines. (http://www.voxforge.org/)

This database interface contains a subset used for speaker recognition defined by
default in a set of CSV files available at
https://www.idiap.ch/software/bob/data/bob/bob.bio.spear/

Feed this file (also defined as resource: ``voxforge``) to ``bob bio pipelines`` as
configuration:

    $ bob bio pipelines vanilla-biometrics -v voxforge <pipeline_name>
"""

from bob.bio.spear.database import VoxforgeBioDatabase

default_protocol = "Default"

if "protocol" not in locals():
    protocol = default_protocol

database = VoxforgeBioDatabase(
    protocol=protocol,
    dataset_protocol_path=None,  # Get from config, or download the protocol definitions
    data_path=None,  # Get from config, or download the data from VoxForge
)
