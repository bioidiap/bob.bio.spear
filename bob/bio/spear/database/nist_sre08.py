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
#        super(NistSre08BioFile, self).__init__(client_id=f.client_id, path=f.path, file_id=f.id)
        super(NistSre08BioFile, self).__init__(client_id='M_ID_X', path=f.path, file_id=f.id)

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
            **kwargs
    ):
        # call base class constructors to open a session to the database
        super(NistSre08BioDatabase, self).__init__(
            name='nist_sre08',
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
