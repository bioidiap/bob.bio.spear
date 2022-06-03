.. vim: set fileencoding=utf-8 :
.. author: Manuel Günther <manuel.guenther@idiap.ch>
.. date: Thu Sep 20 11:58:57 CEST 2012

.. _bob.bio.spear.baselines:

=============================
Executing Baseline Algorithms
=============================

The first thing you might want to do is to execute one of the speaker recognition algorithms that are implemented in ``bob.bio``.

Setting up your Database
----------------------------------------------

For example, you can easily download the audio samples of the `Voxforge`_ database.

By default, ``bob.bio`` does not know, where the wav files are located.
Hence, before running experiments you have to specify the voice database directories.
How this is done is explained in more detail at installation_.


Running Baseline Experiments
------------------------------------------------

To run the baseline experiments, you can use the ``simple`` pipeline by
typing in a bob environment console:

.. code-block:: sh

   $ bob bio pipeline simple

This command is explained in more detail in
:ref:`bob.bio.base.pipeline_simple_intro`.
The ``--help`` option shows you, which other options you can provide.
Here is an extract:

* ``--database``: The database and protocol you want to use. (*config*)
* ``--pipeline``: The pipeline to use. (*config*)
* ``--temp-directory``: The directory where temporary files of the experiments are put to.
* ``--output``: The directory where resulting score files of the experiments are put to.
* ``--verbose``: Increase the verbosity level of the script.
* ``--group``: Specifies the *dev* or *eval* group (or both)

Usually it is a good idea to have at least verbose level 2 (i.e., adding
``--verbose --verbose``, or the short version ``-vv``).

*config* are given into a python file. Some common configurations are aliased to a
shorter name, (e.g. the database config file
``bob/bio/spear/config/database/voxforge.py`` is aliased to ``voxforge``).

Running in Parallel
~~~~~~~~~~~~~~~~~~~

By default (without ``--dask-client`` option), the experiments are still run with dask,
but in one thread on the local machine.

To run the experiments in parallel, you can use a default dask client configuration or
define a customized configuration (see :ref:`bob.pipelines`).

The following command will run the experiments in parallel on the Idiap SGE grid using
the default number of workers::

  $ bob bio pipeline simple -d <database> -p <pipeline> --dask-client sge

To run locally in parallel, you can pass the ``--dask-client local-parallel`` option.



The Algorithms
---------------------------

The algorithms present a set of state-of-the-art speaker recognition algorithms. Here is the list of short-cuts:

* ``gmm``: *Gaussian Mixture Models* (GMM) [Rey00]_.

  - algorithm : :py:class:`bob.bio.spear.algorithm.GMM`

* ``isv``: As an extension of the GMM algorithm, *Inter-Session Variability* (ISV) modeling [Vogt08]_ is used to learn what variations in samples are introduced by identity changes and which not.

  - algorithm : :py:class:`bob.bio.spear.algorithm.ISV`

* ``ivector``: Another extension of the GMM algorithm is *Total Variability* (TV) modeling [Dehak11]_ (aka. I-Vector), which tries to learn a subspace in the GMM super-vector space.

  - algorithm : To be done

.. note::
  The ``ivector`` algorithm needs a lot of training data and fails on small databases such as the `Voxforge`_ database.


Evaluation Results
------------------------------

To evaluate the results,  one can use the ``bob bio evaluate`` command.
Several types of evaluation can be achieved, see
:ref:`bob.bio.base.pipeline_simple_advanced_features` for details.
Particularly, we can enable ROC curves, DET plots, CMC curves and the computation of
EER/HTER or minDCF.


Experiments on different databases
--------------------------------------------------------

To make you more familiar with the tool, we provide you examples of different pipelines
applied on different databases: Voxforge, TIMIT, MOBIO, and NIST SRE 2012.

1. Voxforge dataset
~~~~~~~~~~~~~~~~~~~
`Voxforge`_ is a free database used in free speech recognition engines.
We randomly selected a small part of the english corpus (< 1GB).
It is used as a toy example for our speaker recognition tool since experiment can be
easily run on a local machine, and the results can be obtained in a reasonable amount
of time (< 2h).

Unlike others, this dataset is completely free of charge.

To download the audio files for our experiment, you can use the following command::

  $ bob db download-voxforge ./voxforge_data/

You should then specify to bob where your data is (or where you downloaded it)::

  $ bob config set bob.db.voxforge.directory /your/path/to/voxforge_data/

To then run an experiment, use a command line like::

  $ bob bio pipeline simple --database voxforge --pipeline mfcc60-gmm-voxforge --groups {dev,eval} --output ./results/


In this example, we used the following configuration:

* Energy-based VAD with trained GMM with 2 Gaussians,
* (19 MFCC features + Energy) + First and second derivatives,
* **UBM-GMM** Modelling (with 256 Gaussians).the scoring is done using the linear approximation of the LLR.

The performance of the system can be computed using::

  $ bob bio metrics --eval results/scores-{dev,eval}.csv

On *dev* and *eval*, the scores are:

* ``DEV: EER = 1.7%``
* ``EVAL: HTER = 1.7%``

If you want to run the same experiment on SGE::

  $ bob bio pipeline simple -d voxforge -p mfcc60-gmm-voxforge --groups {dev,eval} --dask-client sge

Another example is to use **ISV** pipeline instead of UBM-GMM (to be done)::

  $ verify.py  -d voxforge -p energy-2gauss -e mfcc-60 -a isv-voxforge -s isv --groups {dev,eval} -g grid

* ``DEV: EER = 1.41%``
* ``EVAL: HTER = 1.52%``

One can also try **JFA** toolchain (to be done)::

  $  verify.py  -d voxforge -p energy-2gauss -e mfcc-60 -a jfa-voxforge -s jfa --groups {dev,eval} -g grid

* ``DEV: EER = 4.04%``
* ``EVAL: HTER = 5.11%``

or also **IVector** toolchain where **Whitening, L-Norm, LDA, WCCN** are used like in this example where the score computation is done using **Cosine distance**::

  $  verify.py  -d voxforge -p energy-2gauss -e mfcc-60 -a ivec-cosine-voxforge -s ivec-cosine --groups {dev,eval} -g grid

* ``DEV: EER = 7.33%``
* ``EVAL: HTER = 13.80%``

The scoring computation can also be done using **PLDA** (to be done)::

  $ verify.py  -d voxforge -p energy-2gauss -e mfcc-60 -a ivec-plda-voxforge -s ivec-plda --groups {dev,eval} -g grid

* ``DEV: EER = 11.33%``
* ``EVAL: HTER = 13.15%``


Note that in the previous examples, our goal is not to optimize the parameters on the DEV set but to provide examples of use.

2. TIMIT dataset
~~~~~~~~~~~~~~~~
`TIMIT`_ is one of the oldest databases (year 1993) used to evaluate speaker recognition systems. In the following example, the processing is done on the development set, and LFCC features are used::

  $ bob bio pipeline simple -vv -d timit -p lfcc60-gmm-timit

Here is the performance of the system on the Development set:

* ``DEV: EER = 2.68%`` (To update)


3. MOBIO dataset
~~~~~~~~~~~~~~~~
This is a more challenging database. The noise and the short duration of the segments make the task of speaker recognition relatively difficult. The following experiment on male group (Mobile-0) uses the 4Hz modulation energy based VAD, and the ISV (with dimU=50) modelling technique::

  $ verify_isv.py -vv -d mobio-audio-male -p mod-4hz -e mfcc-60 -a isv-mobio -s isv --groups {dev,eval} -g demanding

Here is the performance of this system:

* ``DEV: EER = 13.81%``
* ``EVAL: HTER = 10.90%``

To generate the results presented in the ICASSP 2014 paper, please check the script included in the `icassp` folder of the toolbox.
Note that the MOBIO dataset has different protocols, and that are all implemented in `bob.db.mobio`_. But in this toolbox, we provide separately mobile-0 protocol (into filelist format) for simplicity.

4. NIST SRE 2012
~~~~~~~~~~~~~~~~~~
We first invite you to read the paper describing our system submitted to the NIST SRE 2012 Evaluation. The protocols on the development set are the results of a joint work by the I4U group. To reproduce the results, please check this dedicated package::

  https://pypi.python.org/pypi/spear.nist_sre12

.. note::
  For any additional information, please use our mailing list::
  https://groups.google.com/forum/#!forum/bob-devel

.. include:: links.rst
