#!/usr/bin/env python

from bob.bio.spear.database import CPqDReplayBioDatabase


# directory where the wave files are stored
voicepa_wav_directory = "[YOUR_CPQDREPLAY_WAV_DIRECTORY]"
voicepa_input_ext = ".wav"


database_licit = CPqDReplayBioDatabase(
    protocol='cpqdlspk1-licit',
    original_directory=voicepa_wav_directory,
    original_extension=voicepa_input_ext,
    training_depends_on_protocol=True,
)

database_spoof = CPqDReplayBioDatabase(
    protocol='cpqdlspk1-spoof',
    original_directory=voicepa_wav_directory,
    original_extension=voicepa_input_ext,
    training_depends_on_protocol=True,
)

