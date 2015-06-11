#!/usr/bin/env python

import bob.db.mobio
import bob.bio.base

mobio_wav_directory = "[YOUR_MOBIO_WAV_DIRECTORY]"

database = bob.bio.base.database.DatabaseBobZT(
    database = bob.db.mobio.Database(
        original_directory = mobio_wav_directory,
        original_extension = ".wav",
    ),
    name = "mobio-male",
    protocol = 'male',
    models_depend_on_protocol = True,

    all_files_options = { 'gender' : 'male' },
    extractor_training_options = { 'gender' : 'male' },
    projector_training_options = { 'gender' : 'male' },
    enroller_training_options = { 'gender' : 'male' },
    z_probe_options = { 'gender' : 'male' }
)
