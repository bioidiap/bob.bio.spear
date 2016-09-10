#!/usr/bin/env python

from bob.bio.spear.database import MobioBioDatabase
mobio_wav_directory = "[YOUR_MOBIO_WAV_DIRECTORY]"

mobio_audio_male = MobioBioDatabase(
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

mobio_audio_female = MobioBioDatabase(
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
