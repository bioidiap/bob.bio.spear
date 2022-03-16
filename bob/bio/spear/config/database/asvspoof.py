#!/usr/bin/env python

from bob.bio.spear.database import SpearBioDatabase

database_licit = SpearBioDatabase(
    "asvspoof",
    protocol="licit",
)

database_spoof = SpearBioDatabase(
    "asvspoof",
    protocol="spoof",
)
