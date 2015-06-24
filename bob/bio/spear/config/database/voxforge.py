#!/usr/bin/env python

import bob.db.voxforge
import bob.bio.base

#voxforge_wav_directory = "[YOUR_VOXFORGE_WAV_DIRECTORY]"
voxforge_wav_directory = "/idiap/resource/database/VoxForge/audio/original/Trunk/Audio/Main/16kHz_16bit/"

database = bob.bio.base.database.DatabaseBob(
    database = bob.db.voxforge.Database(
        original_directory = voxforge_wav_directory,
        original_extension = ".wav",
    ),
    name = "voxforge",
    protocol = '', # since no protocol is defined
)
