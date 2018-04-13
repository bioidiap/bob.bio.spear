.. vim: set fileencoding=utf-8 :
.. Sun Aug 21 09:26:51 CEST 2016

.. image:: http://img.shields.io/badge/docs-v3.2.0-yellow.svg
   :target: https://www.idiap.ch/software/bob/docs/bob/bob.bio.spear/v3.2.0/index.html
.. image:: http://img.shields.io/badge/docs-latest-orange.svg
   :target: https://www.idiap.ch/software/bob/docs/bob/bob.bio.spear/master/index.html
.. image:: https://gitlab.idiap.ch/bob/bob.bio.spear/badges/v3.2.0/build.svg
   :target: https://gitlab.idiap.ch/bob/bob.bio.spear/commits/v3.2.0
.. image:: https://gitlab.idiap.ch/bob/bob.bio.spear/badges/v3.2.0/coverage.svg
   :target: https://gitlab.idiap.ch/bob/bob.bio.spear/commits/v3.2.0
.. image:: https://img.shields.io/badge/gitlab-project-0000c0.svg
   :target: https://gitlab.idiap.ch/bob/bob.bio.spear
.. image:: http://img.shields.io/pypi/v/bob.bio.spear.svg
   :target: https://pypi.python.org/pypi/bob.bio.spear


===================================
 Run speaker recognition algorithms
===================================

This package is part of the signal-processing and machine learning toolbox
Bob_.
This package is part of the ``bob.bio`` packages, which allow to run comparable and reproducible biometric recognition experiments on publicly available databases.

This package contains functionality to run speaker recognition experiments.
It is an extension to the `bob.bio.base <http://pypi.python.org/pypi/bob.bio.base>`_ package, which provides the basic scripts.
In this package, utilities that are specific for speaker recognition are contained, such as:

* Audio databases
* Voice activity detection preprocessing
* Acoustic feature extractors
* Recognition algorithms based on acoustic features

For further information about ``bob.bio``, please read `its Documentation <https://www.idiap.ch/software/bob/docs/bob/bob.bio.base/v3.2.0/index.html>`_.


Installation
------------

Complete Bob's `installation`_ instructions. Then, to install this package,
run::

  $ conda install bob.bio.spear


Contact
-------

For questions or reporting issues to this software package, contact our
development `mailing list`_.


.. Place your references here:
.. _bob: https://www.idiap.ch/software/bob
.. _installation: https://www.idiap.ch/software/bob/install
.. _mailing list: https://www.idiap.ch/software/bob/discuss