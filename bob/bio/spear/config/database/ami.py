#!/usr/bin/env python

from bob.bio.spear.database import AmiBioDatabase
ami_wav_directory = "[YOUR_AMI_DIRECTORY]"

database = AmiBioDatabase(
    original_directory=ami_wav_directory,
    original_extension=".wav",
)
