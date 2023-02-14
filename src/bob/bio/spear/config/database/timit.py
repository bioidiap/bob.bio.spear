#!/usr/bin/env python

from bob.bio.spear.database import TimitDatabase

default_protocol = "2"

if "protocol" not in locals():
    protocol = default_protocol

database = TimitDatabase(protocol=protocol)
