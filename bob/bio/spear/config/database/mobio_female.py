#!/usr/bin/env python

import bob.bio.base
import bob.db.mobio

mobio_wav_directory = "[YOUR_MOBIO_WAV_DIRECTORY]"

database = bob.bio.base.database.DatabaseBobZT(
    database=bob.db.mobio.Database(
        original_directory=mobio_wav_directory,
        original_extension=".wav",
    ),
    name="mobio-female",
    protocol='female',
    models_depend_on_protocol=True,

    all_files_options={'gender': 'female'},
    extractor_training_options={'gender': 'female'},
    projector_training_options={'gender': 'female'},
    enroller_training_options={'gender': 'female'},
    z_probe_options={'gender': 'female'}
)
