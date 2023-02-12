.. _bob.bio.spear.implemented:

========================================
Tools implemented in bob.bio.spear
========================================

Summary
----------------

Databases
~~~~~~~~~

.. autosummary::
   bob.bio.spear.database


Speech Annotators (VAD)
~~~~~~~~~~~~~~~~~~~~~~~

.. autosummary::
   bob.bio.spear.annotator.Energy_2Gauss
   bob.bio.spear.annotator.Energy_Thr
   bob.bio.spear.annotator.Mod_4Hz


Voice Feature Extractors
~~~~~~~~~~~~~~~~~~~~~~~~

.. autosummary::
   bob.bio.spear.extractor.Cepstral


Databases
---------

.. autoclass:: bob.bio.spear.database.AsvspoofDatabase
.. autoclass:: bob.bio.spear.database.AvspoofDatabase
.. autoclass:: bob.bio.spear.database.MobioDatabase
.. autoclass:: bob.bio.spear.database.NistSRE04To16Database
.. autoclass:: bob.bio.spear.database.TimitDatabase
.. autoclass:: bob.bio.spear.database.VoicepaDatabase
.. autoclass:: bob.bio.spear.database.VoxcelebDatabase
.. autoclass:: bob.bio.spear.database.VoxforgeDatabase


.. include:: links.rst
