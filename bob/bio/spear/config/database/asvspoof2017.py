#!/usr/bin/env python

from bob.bio.spear.database import ASVspoof2017BioDatabase


# directory where the wave files are stored
asvspoof_wav_directory = "[YOUR_ASVSPOOF2017_WAV_DIRECTORY]"
asvspoof_input_ext = ".wav"


database_licit = ASVspoof2017BioDatabase(
    protocol='competition-licit',
    original_directory=asvspoof_wav_directory,
    original_extension=asvspoof_input_ext,
    training_depends_on_protocol=True,
)

database_spoof = ASVspoof2017BioDatabase(
    protocol='competition-spoof',
    original_directory=asvspoof_wav_directory,
    original_extension=asvspoof_input_ext,
    training_depends_on_protocol=True,
)

