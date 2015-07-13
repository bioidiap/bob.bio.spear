#!/usr/bin/env python

import bob.db.verification.filelist
import bob.bio.base

mobio_wav_directory = "[YOUR_MOBIO_WAV_DIRECTORY]"
database = bob.bio.base.database.DatabaseBob(
    database = bob.db.verification.filelist.Database('bob/bio/spear/config/database/mobio/mobile0-male/',
        original_directory = mobio_wav_directory,
        original_extension = ".wav",
    ),
    name = "mobio-male",
    protocol = '',
    
)

