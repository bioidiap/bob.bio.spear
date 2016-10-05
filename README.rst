.. vim: set fileencoding=utf-8 :
.. Sun Aug 21 09:26:51 CEST 2016

.. image:: http://img.shields.io/badge/docs-stable-yellow.png
   :target: http://pythonhosted.org/bob.bio.spear/index.html
.. image:: http://img.shields.io/badge/docs-latest-orange.png
   :target: https://www.idiap.ch/software/bob/docs/latest/bob/bob.bio.spear/master/index.html
.. image:: https://gitlab.idiap.ch/bob/bob.bio.spear/badges/v3.0.0/build.svg
   :target: https://gitlab.idiap.ch/bob/bob.bio.spear/commits/v3.0.0
.. image:: https://img.shields.io/badge/gitlab-project-0000c0.svg
   :target: https://gitlab.idiap.ch/bob/bob.bio.spear
.. image:: http://img.shields.io/pypi/v/bob.bio.spear.png
   :target: https://pypi.python.org/pypi/bob.bio.spear
.. image:: http://img.shields.io/pypi/dm/bob.bio.spear.png
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

For further information about ``bob.bio``, please read `its Documentation <http://pythonhosted.org/bob.bio.base/index.html>`_.


Installation
------------

Follow our `installation`_ instructions. Then, using the Python interpreter
provided by the distribution, bootstrap and buildout this package::

  $ python bootstrap-buildout.py
  $ ./bin/buildout


Contact
-------

For questions or reporting issues to this software package, contact our
development `mailing list`_.


.. Place your references here:
.. _bob: https://www.idiap.ch/software/bob
.. _installation: https://gitlab.idiap.ch/bob/bob/wikis/Installation
.. _mailing list: https://groups.google.com/forum/?fromgroups#!forum/bob-devel
