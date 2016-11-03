#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Amir Mohammadi <amir.mohammadi@idiap.ch>
# Wed 13 Jul 16:43:22 CEST 2016

"""
  NIST SRE 2008 database implementation of bob.bio.db.Database interface.
  It is an extension of an SQL-based database interface, which directly talks to NIST SRE 2008 database, for
  verification experiments (good to use in bob.bio.base framework).
"""


from .database import AudioBioFile
from bob.bio.base.database import BioDatabase, BioFile
import numpy as np
import os

class NistSre08BioFile(AudioBioFile):
    def __init__(self, f):
        """
        Initializes this File object with an File equivalent from the underlying SQl-based interface for
        NIST SRE 2008 database.
        """
        super(NistSre08BioFile, self).__init__(client_id=f.client_id, path=f.path, file_id=f.id)

        self.__f = f
        self.path = os.path.join( os.path.dirname(self.__f.path), self.__f.id)
        
    def load(self, directory=None, extension='.sph'):
        rate, data = self.__f.load(directory, extension)

        data= np.cast['float'](data)
        return rate, data  

    def make_path(self, directory=None, extension=None):
        """Wraps the current path so that a complete path is formed

        Keyword Parameters:

        directory
          An optional directory name that will be prefixed to the returned result.

        extension
          An optional extension that will be suffixed to the returned filename. The
          extension normally includes the leading ``.`` character as in ``.jpg`` or
          ``.hdf5``.

        Returns a string containing the newly generated file path.
        """
        # assure that directory and extension are actually strings
        # create the path
        return str(os.path.join(directory or '', os.path.dirname(self.__f.path), self.__f.id + (extension or '')))


class NistSre08BioDatabase(BioDatabase):
    """
    Implements verification API for querying NIST SRE 2008 database.
    """

    def __init__(
            self,
            protocol='short2-short3-all',
            **kwargs
    ):
        # call base class constructors to open a session to the database
        super(NistSre08BioDatabase, self).__init__(
            name='nist_sre08',
            protocol=protocol,
            **kwargs)


        from bob.db.nist_sre08.query import Database as LowLevelDatabase
        self.__db = LowLevelDatabase()



    def model_ids_with_protocol(self, groups=None, protocol=None, gender=None):
        group = ['eval']
        return self.__db.model_ids(groups=groups, protocol=protocol)

    def objects(self, groups=None, protocol=None, purposes=None, model_ids=None, **kwargs):
        groups = ['eval']
        retval = self.__db.objects(groups=groups, protocol=protocol, purposes=purposes, model_ids=model_ids, **kwargs)
        return [NistSre08BioFile(f) for f in retval]

    def arrange_by_client(self, files):
        """arrange_by_client(files) -> files_by_client

        Arranges the given list of files by client id.
        This function returns a list of lists of File's.

        **Parameters:**

        files : :py:class:`BioFile`
          A list of files that should be split up by `BioFile.client_id`.

        **Returns:**

        files_by_client : [[:py:class:`BioFile`]]
          The list of lists of files, where each sub-list groups the files with the same `BioFile.client_id`
        """
        client_files = {}
        for f in files:
            # we do not include files with unknown client_id
            if f.client_id=='C_ID_X':
              continue
            if f.client_id not in client_files:
                client_files[f.client_id] = []
            client_files[f.client_id].append(f)
        

        files_by_clients = []
        for client in sorted(client_files.keys()):
            if client == 'C_ID_X':
              continue
            files_by_clients.append(client_files[client])
        return files_by_clients


    def training_files(self, step=None, arrange_by_client=False):
        """training_files(step = None, arrange_by_client = False) -> files

        Returns all training files for the given step, and arranges them by client, if desired, respecting the current protocol.
        The files for the steps can be limited using the ``..._training_options`` defined in the constructor.

        **Parameters:**

        step : one of ``('train_extractor', 'train_projector', 'train_enroller')`` or ``None``
          The step for which the training data should be returned.

        arrange_by_client : bool
          Should the training files be arranged by client?
          If set to ``True``, training files will be returned in [[:py:class:`bob.bio.base.database.BioFile`]], where each sub-list contains the files of a single client.
          Otherwise, all files will be stored in a simple [:py:class:`bob.bio.base.database.BioFile`].

        **Returns:**

        files : [:py:class:`BioFile`] or [[:py:class:`BioFile`]]
          The (arranged) list of files used for the training of the given step.
        """

        if step is None:
            training_options = self.all_files_options
        elif step == 'train_extractor':
            training_options = self.extractor_training_options
        elif step == 'train_projector':
            training_options = self.projector_training_options
        elif step == 'train_enroller':
            training_options = self.enroller_training_options
        else:
            raise ValueError(
                "The given step '%s' must be one of ('train_extractor', 'train_projector', 'train_enroller')" % step)

        files = self.sort(self.objects(protocol=self.protocol, groups='eval', **training_options))
        if arrange_by_client:
            return self.arrange_by_client(files)
        else:
            return files
