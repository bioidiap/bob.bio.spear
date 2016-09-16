#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Tiago de Freitas Pereira <tiago.pereira@idiap.ch>
# Wed 20 July 14:43:22 CEST 2016

"""
  Verification API for bob.db.voxforge
"""

from .database import AudioBioFile
from bob.bio.base.database import BioDatabase, BioFile

class VoxforgeBioDatabase(BioDatabase):
    """
    Implements verification API for querying Voxforge database.
    """

    def __init__(self, original_directory=None, original_extension=None, **kwargs):
        # call base class constructors to open a session to the database
        super(VoxforgeBioDatabase, self).__init__(
            name='voxforge', protocol='',
            original_directory=original_directory,
            original_extension=original_extension, **kwargs)

        from bob.db.voxforge.query import Database as LowLevelDatabase
        self.__db = LowLevelDatabase(original_directory=original_directory, original_extension=original_extension)

    def model_ids_with_protocol(self, groups=None, protocol=None, **kwargs):
        """Returns a set of models ids for the specific query by the user.

        Keyword Parameters:

        protocol
            Protocol is ignored in this context, since its choice has no influence on models.

        groups
            The groups to which the subjects attached to the models belong ('dev', 'eval', 'world')

        Returns: A list containing the ids of all models belonging to the given groups.
        """
        return [client.id for client in self.__db.clients(groups=groups, protocol=protocol)]

    def objects(self, protocol=None, purposes=None, model_ids=None,
                groups=None, gender=None):
        """Returns a set of Files for the specific query by the user.

        Keyword Parameters:

        protocol
            Not applicable. VoxForge has only one protocol

        purposes
            The purposes can be either 'enroll', 'probe', or their tuple.
            If 'None' is given (this is the default), it is
            considered the same as a tuple with both possible values.

        model_ids
            Only retrieves the files for the provided list of model ids (claimed
            client id).  If 'None' is given (this is the default), no filter over
            the model_ids is performed.

        groups
            One of the groups ('dev', 'eval', 'world') or a tuple with several of them.
            If 'None' is given (this is the default), it is considered the same as a
            tuple with all possible values.

        gender
            Not applicable

        Returns: A set of Files with the specified properties.
        """

        # now, query the actual Voxforge database
        objects = self.__db.objects(groups=groups,
                                    model_ids=model_ids, purposes=purposes)

        # make sure to return BioFile representation of a file, not the database one
        return [AudioBioFile(client_id=f.client_id, path=f.path, file_id=f.id) for f in objects]
