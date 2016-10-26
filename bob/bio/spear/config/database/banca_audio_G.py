#!/usr/bin/env python

import pkg_resources
import bob.bio.base

banca_wav_directory = "[YOUR_BANCA_WAV_DIRECTORY]"

database = bob.bio.base.database.FileListBioDatabase(
  base_dir = pkg_resources.resource_filename('bob.bio.spear', 'config/database/banca'),
  original_directory = banca_wav_directory,
  original_extension = ".wav",
  name = "banca",
  protocol = "G"
)
