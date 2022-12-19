#!/usr/bin/env python

from bob.bio.spear.database import SpearBioDatabase

database_licit = SpearBioDatabase(
    "voicepa",
    protocol="grandtest-licit",
)

database_spoof = SpearBioDatabase(
    "voicepa",
    protocol="grandtest-spoof",
)
