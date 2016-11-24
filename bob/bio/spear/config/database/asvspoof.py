#!/usr/bin/env python

from bob.bio.spear.database import ASVspoofBioDatabase


# directory where the wave files are stored
asvspoof_wav_directory = "/idiap/temp/pkorshunov/avspoof_cqcc/ASVspoof_d3/prms"
asvspoof_input_ext = ".mat"


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
