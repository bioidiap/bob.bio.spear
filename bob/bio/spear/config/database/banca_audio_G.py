#!/usr/bin/env python

import pkg_resources
import bob.db.bio_filelist

banca_wav_directory = "[YOUR_BANCA_WAV_DIRECTORY]"

database = bob.db.bio_filelist.Database(pkg_resources.resource_filename('bob.bio.db', 'default_configs/banca'),
                                        original_directory=banca_wav_directory,
                                        original_extension=".wav")

