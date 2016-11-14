#!/usr/bin/env python


from bob.bio.spear.database import NistSre05BioDatabase

nist_sre05_directory = "[YOUR_NIST_SRE05_DIRECTORY]"


database = NistSre05BioDatabase(
    original_directory=nist_sre05_directory,
    original_extension='.sph'
)
