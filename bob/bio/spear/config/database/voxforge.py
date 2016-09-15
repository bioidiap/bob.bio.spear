#!/usr/bin/env python

from bob.bio.spear.database import VoxforgeBioDatabase
voxforge_wav_directory = "[YOUR_VOXFORGE_DIRECTORY]"

database = VoxforgeBioDatabase(
    original_directory=voxforge_wav_directory,
    original_extension=".wav",
)
