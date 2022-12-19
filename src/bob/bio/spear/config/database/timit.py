#!/usr/bin/env python

from bob.bio.spear.database import SpearBioDatabase

default_protocol = "2"

if "protocol" not in locals():
    protocol = default_protocol

database = SpearBioDatabase(
    "timit",
    protocol=protocol,
)
