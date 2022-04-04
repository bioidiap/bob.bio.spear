#!/usr/bin/env python

from bob.bio.spear.database import SpearBioDatabase

database_licit = SpearBioDatabase(
    "asvspoof2017",
    protocol="competition-licit",
)

database_spoof = SpearBioDatabase(
    "asvspoof2017",
    protocol="competition-spoof",
)
