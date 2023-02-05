#!/usr/bin/env python

from bob.bio.spear.database import AsvspoofDatabase

database_licit = AsvspoofDatabase(protocol="licit")

database_spoof = AsvspoofDatabase(protocol="spoof")

database = database_licit  # Default for chain loading
