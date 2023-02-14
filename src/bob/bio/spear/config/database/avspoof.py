#!/usr/bin/env python

from bob.bio.spear.database import AvspoofDatabase

database_licit = AvspoofDatabase(protocol="licit")

database_spoof = AvspoofDatabase(protocol="spoof")

database = database_licit  # Default for chain loading
