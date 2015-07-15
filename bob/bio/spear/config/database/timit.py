#!/usr/bin/env python

import bob.db.verification.filelist
import bob.bio.base

timit_wav_directory = "[YOUR_TIMIT_WAV_DIRECTORY]"

database = bob.bio.base.database.DatabaseBob(
    database = bob.db.verification.filelist.Database('bob/bio/spear/config/database/timit/',
        original_directory = timit_wav_directory,
        original_extension = ".wav",
    ),
    name = "timit",
    protocol = '2', 
)
