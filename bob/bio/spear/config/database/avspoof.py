#!/usr/bin/env python

from bob.bio.spear.database import AVspoofBioDatabase


# directory where the wave files are stored
avspoof_wav_directory = "/idiap/temp/pkorshunov/avspoof_cqcc/AVspoof_d3/btas2016/prms/train"
avspoof_input_ext = ".mat"


database_licit = AVspoofBioDatabase(
    protocol='licit',
    original_directory=avspoof_wav_directory,
    original_extension=avspoof_input_ext,
    training_depends_on_protocol=True,
)

database_spoof = AVspoofBioDatabase(
    protocol='spoof',
    original_directory=avspoof_wav_directory,
    original_extension=avspoof_input_ext,
    training_depends_on_protocol=True,
)

