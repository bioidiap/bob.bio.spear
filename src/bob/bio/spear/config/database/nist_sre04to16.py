#!/usr/bin/env python
# @author: Yannick Dayer <yannick.dayer@idiap.ch>
# @date: Tue 12 Apr 2022 09:36:40 UTC+02

"""Default configuration file for the NIST-SRE database.

Use this file (defined as ``nist-sre04to16`` in ``entry-points``) as parameter to the
``bob bio pipeline`` commands::

    $ bob bio pipeline simple nist-sre04to16 [...]

This database uses the NIST-SRE 2016 to evaluate the performance of a system. Other
datasets from NIST are used as training data.

Three protocols are available. They have the same dev and eval groups. The differences
are in the training set:
    - core: Selected set of files from the NIST-SRE database with labels.
    - core-aug: Augmented data with reverberation or background noise (music, noise,
        speech/babble).
    - unlabeled: Includes data that were not labeled.


Bob does not provide the data files for its databases.
After downloading the NIST-SRE database files, configure their location using::

    $ bob config set bob.db.nist_sre04to16.directory /path/to/nist-sre-root/

This folder (pointed to by the ``bob config`` command) should contain the following
subfolders:
    - ``nist_sre/SRE16``: used for dev and eval groups for enrollment and scoring.
    - ``Switchboard_2_Phase_II/dbase``: used for training.
    - ``Switchboard_2_Phase_III/dbase``: used for training.
    - ``Switchboard_Cellular_Part1/dbase``: used for training.
    - ``Switchboard_Cellular_Part2/dbase``: used for training.
    - ``nist_sre/SRE04``: used for training.
    - ``nist_sre/SRE05``: used for training.
    - ``nist_sre/SRE06``: used for training.
    - ``nist_sre/SRE08``: used for training.
    - ``nist_sre/SRE10``: used for training.
"""

from bob.bio.spear.database import NistSRE04To16Database

if "protocol" not in locals():
    protocol = "core"

database = NistSRE04To16Database(protocol=protocol)
