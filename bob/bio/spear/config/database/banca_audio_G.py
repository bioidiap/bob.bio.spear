#!/usr/bin/env python

import pkg_resources
import bob.bio.base
from bob.bio.spear.database import AudioBioFile

banca_wav_directory = "[YOUR_BANCA_WAV_DIRECTORY]"

database = bob.bio.base.database.FileListBioDatabase(pkg_resources.resource_filename('bob.bio.spear', 'config/database/banca'),
                                                     'banca',
                                                     bio_file_class=AudioBioFile,
                                                     protocol='G',
                                                     original_directory=banca_wav_directory,
                                                     original_extension=".wav")
