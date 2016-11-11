#!/usr/bin/env python


from bob.bio.spear.database import NistSre12BioDatabase

nist_sre12_directory = "[YOUR_NIST_SRE12_DIRECTORY]"


database = NistSre12BioDatabase(
    original_directory=nist_sre12_directory,
    original_extension='.sph'
)
