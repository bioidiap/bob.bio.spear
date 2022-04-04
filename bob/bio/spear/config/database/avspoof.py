#!/usr/bin/env python

from bob.bio.spear.database import SpearBioDatabase

database_licit = SpearBioDatabase(
    "avspoof",
    protocol="licit",
)

database_spoof = SpearBioDatabase(
    "avspoof",
    protocol="spoof",
)
