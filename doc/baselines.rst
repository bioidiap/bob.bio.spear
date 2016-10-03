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
How this is done is explained in more detail in the :ref:`bob.bio.base.installation`.


Running Baseline Experiments
------------------------------------------------

To run the baseline experiments, you can use the ``./bin/verify.py`` script by just going to the console and typing:

.. code-block:: sh

   $ ./bin/verify.py

This script is explained in more detail in :ref:`bob.bio.base.experiments`.
The ``./bin/verify.py --help`` option shows you, which other options you have.
Here is an almost complete extract:

* ``--database``: The database and protocol you want to use.
* ``--algorithms``: The recognition algorithms that you want to execute.
* ``--all``: Execute all algorithms that are implemented.
* ``--temp-directory``: The directory where temporary files of the experiments are put to.
* ``--result-directory``: The directory where resulting score files of the experiments are put to.
* ``--evaluate``: After running the experiments, the resulting score files will be evaluated, and the result is written to console.
* ``--dry-run``: Instead of executing the algorithm (or the evaluation), only print the command that would have been executed.
* ``--verbose``: Increase the verbosity level of the script.
  By default, only the commands that are executed are printed, and the rest of the calculation runs quietly.
  You can increase the verbosity by adding the ``--verbose`` parameter repeatedly (up to three times).

Usually it is a good idea to have at least verbose level 2 (i.e., calling ``./bin/verify.py --verbose --verbose``, or the short version ``./bin/verify.py -vv``).

Running in Parallel
~~~~~~~~~~~~~~~~~~~

To run the experiments in parallel, as usual you can define an SGE grid configuration, or run with parallel threads on the local machine.
For the ``./bin/verify.py`` script, the grid configuration is adapted to each of the algorithms.
Hence, to run in the SGE grid, you can simply add the ``--grid`` command line option, without parameters.
Similarly, to run the experiments in parallel on the local machine, simply add a ``--parallel <N>`` option, where ``<N>`` specifies the number of parallel jobs you want to execute.

When running the algorithms from the `bob.bio.gmm`_ package in parallel, the specialized scripts are executed.
This will speed up the training of the UBM (and possible additional steps) tremendously.


The Algorithms
---------------------------

The algorithms present a set of state-of-the-art speaker recognition algorithms. Here is the list of short-cuts:

* ``gmm``: *Gaussian Mixture Models* (GMM) `[Rey00]`.

  - algorithm : :py:class:`bob.bio.gmm.algorithm.GMM`

* ``isv``: As an extension of the GMM algorithm, *Inter-Session Variability* (ISV) modeling `[Vogt08]` is used to learn what variations in samples are introduced by identity changes and which not.

  - algorithm : :py:class:`bob.bio.gmm.algorithm.ISV`

* ``ivector``: Another extension of the GMM algorithm is *Total Variability* (TV) modeling `[Dehak11]` (aka. I-Vector), which tries to learn a subspace in the GMM super-vector space.

  - algorithm : :py:class:`bob.bio.gmm.algorithm.IVector`

.. note::
  The ``ivector`` algorithm needs a lot of training data and fails on small databases such as the `Voxforge`_ database.


Evaluation Results
------------------------------

To evaluate the results,  one can use ``./bin/evaluate.py`` command.
Several types of evaluation can be achieved, see :ref:`bob.bio.base.evaluate` for details.
Particularly, here we can enable ROC curves, DET plots, CMC curves and the computation of EER/HTER or minDCF.


Experiments on different databases
--------------------------------------------------------

To make you more familiar with the tool, we provide you examples of different toolchains applied on different databases: Voxforge, BANCA, TIMIT, MOBIO, and NIST SRE 2012.

`Voxforge`_ is a free database used in free speech recognition engines. We randomly selected a small part of the english corpus (< 1GB).  It is used as a toy example for our speaker recognition tool since experiment can be easily run on a local machine, and the results can be obtained in a reasonnable amount of time (< 2h).

Unlike TIMIT and BANCA, this dataset is completely free of charge.

More details about how to download the audio files used in our experiments, and how the data is split into Training, Development and Evaluation set can be found here::

  https://pypi.python.org/pypi/bob.db.voxforge

One example of command line is::

  $ bin/verify.py  -d voxforge -p energy-2gauss -e mfcc-60 -a gmm-voxforge -s ubm_gmm --groups {dev,eval}


In this example, we used the following configuration:

* Energy-based VAD,
* (19 MFCC features + Energy) + First and second derivatives,
* **UBM-GMM** Modelling (with 256 Gaussians), the scoring is done using the linear approximation of the LLR.

The performance of the system on DEV and EVAL are:

* ``DEV: EER = 1.89%``
* ``EVAL: HTER = 1.56%``

If you want to run the same experiment on SGE::

  $ bin/verify.py  -d voxforge -p energy-2gauss -e mfcc-60 -a gmm-voxforge -s ubm_gmm --groups {dev,eval}  -g grid


If you want to run the parallel implementation of the UBM on the SGE::

  $ bin/verify_gmm.py  -d voxforge -p energy-2gauss -e mfcc-60 -a gmm-voxforge -s ubm_gmm_sge --groups {dev,eval} -g grid


If you want to run the parallel implementation of the UBM on your local machine::

  $ bin/verify_gmm.py  -d voxforge -p energy-2gauss -e mfcc-60 -a gmm-voxforge -s ubm_gmm_local --groups {dev,eval} -g local

Another example is to use **ISV** toolchain instead of UBM-GMM::

  $ bin/verify.py  -d voxforge -p energy-2gauss -e mfcc-60 -a isv-voxforge -s isv --groups {dev,eval} -g grid

* ``DEV: EER = 1.41%``
* ``EVAL: HTER = 1.52%``

One can also try **JFA** toolchain::

  $  bin/verify.py  -d voxforge -p energy-2gauss -e mfcc-60 -a jfa-voxforge -s jfa --groups {dev,eval} -g grid

* ``DEV: EER = 4.04%``
* ``EVAL: HTER = 5.11%``

or also **IVector** toolchain where **Whitening, L-Norm, LDA, WCCN** are used like in this example where the score computation is done using **Cosine distance**::

  $  bin/verify.py  -d voxforge -p energy-2gauss -e mfcc-60 -a ivec-cosine-voxforge -s ivec-cosine --groups {dev,eval} -g grid

* ``DEV: EER = 7.33%``
* ``EVAL: HTER = 13.80%``

The scoring computation can also be done using **PLDA**::

  $ bin/verify.py  -d voxforge -p energy-2gauss -e mfcc-60 -a ivec-plda-voxforge -s ivec-plda --groups {dev,eval} -g grid

* ``DEV: EER = 11.33%``
* ``EVAL: HTER = 13.15%``


Note that in the previous examples, our goal is not to optimize the parameters on the DEV set but to provide examples of use.

2. BANCA dataset
~~~~~~~~~~~~~~~~
`BANCA`_ is a simple bimodal database with relatively clean data. The results are already very good with a simple baseline UBM-GMM system. An example of use can be::

  $ bin/verify.py -vv -d banca-audio -p energy-2gauss -e mfcc-60 -a gmm-banca -s banca_G --groups {dev,eval}

The configuration in this example is similar to the previous one with the only difference of using the regular LLR instead of its linear approximation.

Here is the performance of this system:

* ``DEV: EER = 0.91%``
* ``EVAL: EER = 0.75%``


3. TIMIT dataset
~~~~~~~~~~~~~~~~
`TIMIT`_ is one of the oldest databases (year 1993) used to evaluate speaker recognition systems. In the following example, the processing is done on the development set, and LFCC features are used::

  $ bin/verify.py -vv -d timit -p energy-2gauss -e lfcc-60 -a gmm-timit -s timit

Here is the performance of the system on the Development set:

* ``DEV: EER = 2.68%``


4. MOBIO dataset
~~~~~~~~~~~~~~~~
This is a more challenging database. The noise and the short duration of the segments make the task of speaker recognition relatively difficult. The following experiment on male group (Mobile-0) uses the 4Hz modulation energy based VAD, and the ISV (with dimU=50) modelling technique::

  $ bin/verify_isv.py -vv -d mobio-audio-male -p mod-4hz -e mfcc-60 -a isv-mobio -s isv --groups {dev,eval} -g demanding

Here is the performance of this system:

* ``DEV: EER = 13.81%``
* ``EVAL: HTER = 10.90%``

To generate the results presented in the ICASSP 2014 paper, please check the script included in the `icassp` folder of the toolbox.
Note that the MOBIO dataset has different protocols, and that are all implemented in `bob.db.mobio`_. But in this toolbox, we provide separately mobile-0 protocol (into filelist format) for simplicity.

5. NIST SRE 2012
~~~~~~~~~~~~~~~~~~
We first invite you to read the paper describing our system submitted to the NIST SRE 2012 Evaluation. The protocols on the development set are the results of a joint work by the I4U group. To reproduce the results, please check this dedicated package::

  https://pypi.python.org/pypi/spear.nist_sre12

.. note::
  For any additional information, please use our mailing list::
  https://groups.google.com/forum/#!forum/bob-devel

.. include:: links.rst


