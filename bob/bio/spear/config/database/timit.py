#!/usr/bin/env python

import pkg_resources
import bob.bio.base
from bob.bio.spear.database import AudioBioFile

timit_wav_directory = "[YOUR_TIMIT_WAV_DIRECTORY]"

database = bob.bio.base.database.FileListBioDatabase(pkg_resources.resource_filename('bob.bio.spear', 'config/database/timit'),
                                                     'timit',
                                                     bio_file_class=AudioBioFile,
                                                     protocol='2',
                                                     original_directory=timit_wav_directory,
                                                     original_extension=".wav")
