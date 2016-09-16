#!/usr/bin/env python

from bob.bio.spear.database import MobioBioDatabase
mobio_wav_directory = "[YOUR_MOBIO_WAV_DIRECTORY]"

database = MobioBioDatabase(
    original_directory=mobio_wav_directory,
    original_extension=".wav",
    protocol='male',
    models_depend_on_protocol=True,
    all_files_options={'gender': 'male'},
    extractor_training_options={'gender': 'male'},
    projector_training_options={'gender': 'male'},
    enroller_training_options={'gender': 'male'},
    z_probe_options={'gender': 'male'}
)

