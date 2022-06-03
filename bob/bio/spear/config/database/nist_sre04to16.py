#!/usr/bin/env python
# @author: Yannick Dayer <yannick.dayer@idiap.ch>
# @date: Tue 12 Apr 2022 09:36:40 UTC+02

"""Default configuration file for the NIST-SRE database.

Use this file (defined as ``nist-sre`` in ``entry-points``) as parameter to the
``bob bio pipeline`` commands::

    $ bob bio pipeline simple -d nist-sre [...]

Each of those three protocols have the same dev and eval groups. The differences are in
**the training set**:
    - core: Selected set of files from the NIST-SRE database with labels.
    - core-aug: Augmented data with reverberation or background noise (music, noise,
        speech/babble).
    - unlabeled: Different data that were not labeled.

To get the augmented data, please use the correct pipeline configuration. # TODO specify which one
"""

from bob.bio.spear.database import SpearBioDatabase

if "protocol" not in locals():
    protocol = "core"

database = SpearBioDatabase(
    "nist_sre04to16",
    protocol=protocol,
    data_ext=".sph",
    force_sample_rate=16000,
)
