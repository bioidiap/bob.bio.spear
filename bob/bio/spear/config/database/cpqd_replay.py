#!/usr/bin/env python

from bob.bio.spear.database import CPqDReplayBioDatabase


# directory where the wave files are stored
cpqd_replay_wav_directory = "/idiap/resource/database/CPqD/"
cpqd_replay_input_ext = ".wav"


database_licit = CPqDReplayBioDatabase(
    protocol='cpqdlspk1-licit',
    original_directory=cpqd_replay_wav_directory,
    original_extension=cpqd_replay_input_ext,
    training_depends_on_protocol=True,
)

database_spoof = CPqDReplayBioDatabase(
    protocol='cpqdlspk1-spoof',
    original_directory=cpqd_replay_wav_directory,
    original_extension=cpqd_replay_input_ext,
    training_depends_on_protocol=True,
)

