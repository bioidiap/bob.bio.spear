#!/usr/bin/env python

import bob.bio.db

voxforge_wav_directory = "[YOUR_VOXFORGE_DIRECTORY]"

database = bob.bio.spear.database.VoxforgeBioDatabase(
    original_directory=voxforge_wav_directory,
    original_extension=".wav",
)
