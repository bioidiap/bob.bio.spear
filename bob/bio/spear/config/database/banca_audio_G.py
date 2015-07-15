#!/usr/bin/env python

import bob.db.verification.filelist
import bob.bio.base

banca_wav_directory = "[YOUR_BANCA_WAV_DIRECTORY]"

database = bob.bio.base.database.DatabaseBob(
    database = bob.db.verification.filelist.Database('bob/bio/spear/config/database/banca/',
        original_directory = banca_wav_directory,
        original_extension = ".wav",
    ),
    name = "banca",
    protocol = 'G', 
)
