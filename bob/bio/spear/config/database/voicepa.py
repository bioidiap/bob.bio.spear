#!/usr/bin/env python

from bob.bio.spear.database import VoicePABioDatabase


# directory where the wave files are stored
voicepa_wav_directory = "[YOUR_VOICEPA_WAV_DIRECTORY]"
voicepa_input_ext = ".wav"


database_licit = VoicePABioDatabase(
    protocol='grandtest-licit',
    original_directory=voicepa_wav_directory,
    original_extension=voicepa_input_ext,
    training_depends_on_protocol=True,
)

database_spoof = VoicePABioDatabase(
    protocol='grandtest-spoof',
    original_directory=voicepa_wav_directory,
    original_extension=voicepa_input_ext,
    training_depends_on_protocol=True,
)

