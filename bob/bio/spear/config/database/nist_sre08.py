#!/usr/bin/env python


from bob.bio.spear.database import NistSre08BioDatabase

nist_sre08_directory = "[YOUR_NIST_SRE08_DIRECTORY]"


database = NistSre08BioDatabase(
    original_directory=nist_sre08_directory,
    original_extension='.sph'
)
