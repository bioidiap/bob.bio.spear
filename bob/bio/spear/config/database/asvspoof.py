#!/usr/bin/env python

from bob.bio.spear.database import ASVspoofBioDatabase


# directory where the wave files are stored
asvspoof_wav_directory = "[YOUR_ASVSPOOF_WAV_DIRECTORY]"
asvspoof_input_ext = ".wav"


database_licit = ASVspoofBioDatabase(
    protocol='licit',
    original_directory=asvspoof_wav_directory,
    original_extension=asvspoof_input_ext,
    training_depends_on_protocol=True,
)

database_spoof = ASVspoofBioDatabase(
    protocol='spoof',
    original_directory=asvspoof_wav_directory,
    original_extension=asvspoof_input_ext,
    training_depends_on_protocol=True,
)
