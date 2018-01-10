#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Tiago de Freitas Pereira <tiago.pereira@idiap.ch>
# Wed 20 July 14:43:22 CEST 2016

from bob.bio.base.database.file import BioFile
import scipy
import numpy


class AudioBioFile(BioFile):
    def __init__(self, client_id, path, file_id, **kwargs):
        """
        Initializes this File object with an File equivalent for
        VoxForge database.
        """
        super(AudioBioFile, self).__init__(
            client_id=client_id, path=path, file_id=file_id, **kwargs)

    def load(self, directory=None, extension='.wav'):
        rate, audio = scipy.io.wavfile.read(
            self.make_path(directory, extension))
        # We consider there is only 1 channel in the audio file => data[0]
        data = numpy.cast['float'](audio)
        return rate, data
