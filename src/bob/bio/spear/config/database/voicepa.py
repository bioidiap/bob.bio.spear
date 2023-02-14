#!/usr/bin/env python

from bob.bio.spear.database import VoicepaDatabase

database_licit = VoicepaDatabase(protocol="grandtest-licit")

database_spoof = VoicepaDatabase(protocol="grandtest-spoof")

database = database_licit  # Default for chain loading
