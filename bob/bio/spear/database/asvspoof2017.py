#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Pavel Korshunov <pavel.korshunov@idiap.ch>
# Tue 11 Oct 15:43:22 2016

"""
  This is the implementation of ASVspoof2017 Competition database high level interface that can be used in 
  `bob.bio.base` framework. IMPORTANT: this interface is not suitable for running the verification experiments,
  since ASVspoof2017 does not have verification protocols. This interface is just a simple wrapper around
  presentation attack detection protocols, providing data for `licit` (real access) and `spoof` (attacks) scenarios,
  so that training scripts provided by `bob.bio.base` can be run on this database. 
  Also, this is an extension of a FileList based database interface.
"""

from bob.bio.base.database import BioDatabase
from bob.bio.spear.database import AudioBioFile


class ASVspoof2017BioFile(AudioBioFile):
    def __init__(self, f):
        """
        Initializes this File object with an File equivalent from the underlying SQl-based interface for
        ASVspoof2017 database.
        """
        super(ASVspoof2017BioFile, self).__init__(client_id=f.client_id, path=f.path, file_id=f.id)

        self.__f = f


class ASVspoof2017BioDatabase(BioDatabase):
    """
    Implements verification API for querying ASVspoof2017 database.
    """

    def __init__(self, **kwargs):
        # call base class constructors to open a session to the database
        super(ASVspoof2017BioDatabase, self).__init__(name='asvspoof2017', **kwargs)

        from bob.db.asvspoof2017.query import Database as LowLevelDatabase
        self.__db = LowLevelDatabase()

        self.low_level_group_names = ('train', 'dev', 'eval')
        self.high_level_group_names = ('world', 'dev', 'eval')

    def model_ids_with_protocol(self, groups=None, protocol=None, gender=None):
        groups = self.convert_names_to_lowlevel(groups, self.low_level_group_names, self.high_level_group_names)

        return [client.id for client in self.__db.clients(groups=groups, gender=gender)]

    def objects(self, protocol=None, purposes=None, model_ids=None, groups=None, **kwargs):

        # convert group names from the conventional names in verification experiments to the internal database names
        if groups is None:  # all groups are assumed
            groups = self.high_level_group_names
        matched_groups = self.convert_names_to_lowlevel(groups, self.low_level_group_names, self.high_level_group_names)

        # this conversion of the protocol with appended '-licit' or '-spoof' is a hack for verification experiments.
        # To adapt spoofing databases to the verification experiments, we need to be able to split a given protocol
        # into two parts: when data for licit (only real/genuine data is used) and data for spoof (attacks are used instead
        # of real data) is used in the experiment. Hence, we use this trick with appending '-licit' or '-spoof' to the
        # protocol name, so we can distinguish these two scenarios.
        # By default, if nothing is appended, we assume licit protocol.
        # The distinction between licit and spoof is expressed via purposes parameters, but
        # the difference is the terminology only.

        # lets check if we have an appendix to the protocol name
        appendix = None
        if protocol:
            appendix = protocol.split('-')[-1]

        # if protocol was empty or there was no correct appendix, we just assume the 'licit' option
        if not (appendix == 'licit' or appendix == 'spoof'):
            appendix = 'licit'
        else:
            # put back everything except the appendix into the protocol
            protocol = '-'.join(protocol.split('-')[:-1])

        # if protocol was empty, we set it to the default 'competition'
        if not protocol:
            protocol = 'competition'

        correct_purposes = purposes
        # licit protocol is for real access data only
        if appendix == 'licit':
            # by default we assume all real data, since this database has not enroll data
            if purposes is None:
                correct_purposes = ('genuine',)

        # spoof protocol uses real data for enrollment and spoofed data for probe
        # so, probe set is the same as attack set
        if appendix == 'spoof':
            # we return attack data only, since this database does not have enroll
            if purposes is None:
                correct_purposes = ('spoof',)
            # otherwise replace 'probe' with 'attack'
            elif isinstance(purposes, (tuple, list)):
                correct_purposes = []
                for purpose in purposes:
                    if purpose == 'probe':
                        correct_purposes += ['spoof']
                    else:
                        correct_purposes += [purpose]
            elif purposes == 'probe':
                correct_purposes = ('spoof',)

        # now, query the actual ASVspoof2017 database
        objects = self.__db.objects(protocol=protocol, groups=matched_groups, purposes=correct_purposes,
                                    **kwargs)
        # make sure to return BioFile representation of a file, not the database one
        return [ASVspoof2017BioFile(f) for f in objects]

    def annotations(self, file):
        return None
