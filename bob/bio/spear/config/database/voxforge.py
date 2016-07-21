#!/usr/bin/env python

import bob.bio.db

voxforge_wav_directory = "/idiap/resource/database/VoxForge/audio/original/Trunk/Audio/Main/16kHz_16bit"

database = bob.bio.db.VoxforgeBioDatabase(
    original_directory=voxforge_wav_directory,
    original_extension=".wav",
)
