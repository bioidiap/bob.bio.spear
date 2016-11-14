#!/usr/bin/env python


from bob.bio.spear.database import NistSre06BioDatabase

nist_sre06_directory = "[YOUR_NIST_SRE06_DIRECTORY]"


database = NistSre06BioDatabase(
    original_directory=nist_sre06_directory,
    original_extension='.sph'
)
