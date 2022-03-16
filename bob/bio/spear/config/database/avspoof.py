#!/usr/bin/env python

from bob.bio.spear.database import SpearBioDatabase

# directory where the wave files are stored
avspoof_wav_directory = "[YOUR_AVSPOOF_WAV_DIRECTORY]"
avspoof_input_ext = ".wav"


database_licit = SpearBioDatabase(
    "avspoof",
    protocol="licit",
)

database_spoof = SpearBioDatabase(
    "avspoof",
    protocol="spoof",
)
