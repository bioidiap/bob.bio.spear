#!/usr/bin/env python

import pkg_resources
import bob.db.bio_filelist

timit_wav_directory = "[YOUR_TIMIT_WAV_DIRECTORY]"

database = bob.db.bio_filelist.Database(pkg_resources.resource_filename('bob.bio.spear', 'config/database/timit'),
                                        original_directory=timit_wav_directory,
                                        original_extension=".wav")
