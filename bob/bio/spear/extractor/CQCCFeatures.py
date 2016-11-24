#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Pavel Korshunov <pavel.korshunov@idiap.ch>
# Wed 23 Nov 17:13:22 CEST 2016
#


from __future__ import print_function

import bob.io.base
import numpy

import logging
logger = logging.getLogger("bob.bio.spear")
logger.setLevel(logging.DEBUG)

from bob.bio.base.extractor import Extractor
from bob.bio.base.preprocessor import Preprocessor


class CQCCFeatures(Preprocessor, Extractor):
    """
    This class should be used as a preprocessor (converts matlab data into HDF5) and an extractor (reads saved data)

    Converts pre-computed with Matlab CQCC features into numpy array suitable for Bob-based experiments.
    CQCC features are obtained using CQCC Matlab toolkit from http://audio.eurecom.fr/content/software
    The features are originally proposed in the following paper:
    Todisco, Massimiliano; Delgado, Héctor; Evans, Nicholas
    "Articulation rate filtering of CQCC features for automatic speaker verification", INTERSPEECH 2016,
    Annual Conference of the International Speech Communication Association, September 8-12, 2016, San Francisco, USA
    """

    def __init__(
            self,
            split_training_data_by_client=False,
            features_mask=numpy.zeros(90),  # mask of which features to read
            **kwargs
    ):
        # call base class constructor with its set of parameters
        Preprocessor.__init__(self, read_original_data=self.read_matlab_files, **kwargs)
        Extractor.__init__(self, requires_training=False, split_training_data_by_client=split_training_data_by_client,
                           **kwargs)
        self.features_mask = features_mask

    def read_matlab_files(self, biofile, directory, extension):
        """
        We have no preprocessing, so this function does nothing
        """
        import bob.io.matlab
        # return the numpy array read from the data_file
        data_path = biofile.make_path(directory, extension)
        return bob.io.base.load(data_path)


#    def write_data(self, data, data_file, compression=0):
#        """
#        We have no preprocessing, so this function does nothing
#        """
#        pass
#
#    def read_data(self, data_file):
#        """
#        Here we read Matlab file and extract the CQCC features
#        They will be passed to the __call__() function by the extractor of bob.bio.base
#        """
#        # we require bob.io.matlab to be available at this moment but it does not need to be available
#        # in the bob.bio.spear package as a whole
#        import bob.io.matlab
#        # return the numpy array read from the data_file
#        return bob.io.base.load(data_file)

    def __call__(self, input_data, annotations):
        """
        When this function is called in the capacity of Preprocessor, we do nothing.
        When it is called as an Extractor, we assume that Matlab features were read correctly,
        so we can process them
        """

        if input_data is None:  # acting as an empty Preprocessor
            return 0  # do not return None to avoid preprocessing warnings

        # From now on we are acting as an Extractor that has received correctly read Matlab CQCC features

        features = input_data
        # return features that we have just read with self.read_data()
        assert(self.features_mask.shape[0] < input_data.shape[0])
        if self.features_mask.shape[0] < input_data.shape[0]:
            print("In Preprocesing, creating masking array")
            features = input_data[self.features_mask]

        # transpose, because of the way original Matlab-based features are
        # computed
        return numpy.transpose(features)


cqcc_reader = CQCCFeatures()
