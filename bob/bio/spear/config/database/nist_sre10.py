#!/usr/bin/env python


from bob.bio.spear.database import NistSre10BioDatabase

nist_sre10_directory = "[YOUR_NIST_SRE10_DIRECTORY]"


database = NistSre10BioDatabase(
    original_directory=nist_sre10_directory,
    original_extension='.sph'
)
