.. vim: set fileencoding=utf-8 :
.. Elie Khoury <Elie.Khoury@idiap.ch>
.. Fri 12 Jun 11:34:43 CEST 2015
.. Copyright (C) 2012-2015 Idiap Research Institute, Martigny, Switzerland



.. _bob.bio.spear:


SPEAR: A Speaker Recognition Toolkit based on Bob
====================================================


This package is part of the ``bob.bio`` packages, which provide open source tools to run comparable and reproducible biometric recognition experiments.
In this package, tools for executing speaker recognition experiments are provided.

This includes:

* Speaker Recognition databases and their according protocols
* Voice activity detection
* Feature extraction
* Recognition/Verification tools

Notice that most of the machine learning tools (GMM, ISV, JFA, IVectors) are now handle by  bob.bio.gmm

`spear`_ is adapted to run speaker verification/recognition experiments with the SGE grid infrastructure at Idiap.

If you use this package and/or its results, please cite the following paper published at ICASSP 2014::

    @inproceedings{spear,
      author = {Khoury, E. and El Shafey, L. and Marcel, S.},
      title = {Spear: An open source toolbox for speaker recognition based on {B}ob},
      booktitle = {IEEE Intl. Conf. on Acoustics, Speech and Signal Processing (ICASSP)},
      year = {2014},
      url = {http://publications.idiap.ch/downloads/papers/2014/Khoury_ICASSP_2014.pdf},
    }

For more detailed information about the structure of the ``bob.bio`` packages, please refer to the documentation of :ref:`bob.bio.base <bob.bio.base>`.
Particularly, the installation of this and other ``bob.bio`` packages, please read the :ref:`bob.bio.base.installation`.

In the following, we provide more detailed information about the particularities of this package only.

===========
Users Guide
===========

.. toctree::
   :maxdepth: 2

   baselines
   implementation
   references


================
Reference Manual
================

.. toctree::
   :maxdepth: 2

   implemented


.. include:: links.rst

.. todolist::

