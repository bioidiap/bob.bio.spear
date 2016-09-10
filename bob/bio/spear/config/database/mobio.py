#!/usr/bin/env python

import bob.bio.spear

mobio_wav_directory = "[YOUR_MOBIO_WAV_DIRECTORY]"

mobio_audio_male = bob.bio.spear.database.MobioBioDatabase(
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

mobio_audio_female = bob.bio.spear.database.MobioBioDatabase(
    original_directory=mobio_wav_directory,
    original_extension=".wav",
    protocol='female',
    models_depend_on_protocol=True,
    all_files_options={'gender': 'female'},
    extractor_training_options={'gender': 'female'},
    projector_training_options={'gender': 'female'},
    enroller_training_options={'gender': 'female'},
    z_probe_options={'gender': 'female'}
)
