.. vim: set fileencoding=utf-8 :
.. Elie Khoury <Elie.Khoury@idiap.ch>
.. Fri 12 Jun 11:34:43 CEST 2015
.. Copyright (C) 2012-2015 Idiap Research Institute, Martigny, Switzerland



.. _bob.bio.spear:


SPEAR: A Speaker Recognition Toolkit based on Bob
====================================================


.. todo::
   Update the documentation so that it is conform with the other ``bob.bio`` packages.

SPEAR is a speaker recognition toolkit based on Bob, designed to run speaker verification/recognition
experiments . It was originally inspired from facereclib tool:
https://pypi.python.org/pypi/facereclib

`SPEAR`_ is designed in a way that it should be easily possible to execute experiments combining different mixtures of:

* Speaker Recognition databases and their according protocols
* Voice activity detection
* Feature extraction
* Recognition/Verification tools

Notice that most of the machine learning tools (GMM, ISV, JFA, IVectors) are now handle by  bob.bio.gmm

In any case, results of these experiments will directly be comparable when the same dataset is employed.

`SPEAR`_ is adapted to run speaker verification/recognition experiments with the SGE grid infrastructure at Idiap.

If you use this package and/or its results, please cite the following paper published at ICASSP 2014::
    @inproceedings{spear,
      author = {Khoury, E. and El Shafey, L. and Marcel, S.},
      title = {Spear: An open source toolbox for speaker recognition based on {B}ob},
      booktitle = {IEEE Intl. Conf. on Acoustics, Speech and Signal Processing (ICASSP)},
      year = {2014},
      url = {http://publications.idiap.ch/downloads/papers/2014/Khoury_ICASSP_2014.pdf},
    }


I- Installation
--------------------

`spear`_ is based on the `BuildOut`_ python linking system. You only need to use buildout to bootstrap and have a working environment ready for
experiments::

  $ python bootstrap
  $ ./bin/buildout

This also requires that bob (>= 2.0) is installed.


II- Running experiments
------------------------

The above two commands will automatically download all desired packages from `pypi`_ and generate some scripts in the bin directory, including the following scripts::

   $ bin/spkverif_gmm.py
   $ bin/spkverif_isv.py
   $ bin/spkverif_jfa.py
   $ bin/spkverif_ivector.py
   $ bin/para_ubm_spkverif_isv.py
   $ bin/para_ubm_spkverif_ivector.py
   $ bin/para_ubm_spkverif_gmm.py
   $ bin/fusion_llr.py
   $ bin/evaluate.py
   $ bin/det.py

The first four toolchains are the basic toolchains for GMM, ISV, JFA and I-Vector. The next three toolchains are the parallel implementation of GMM, ISV, and I-Vector.

To use the 7 first (main) toolchains you have to specify at least four command line parameters (see also the ``--help`` option):

* ``--database``: The configuration file for the database
* ``--preprocessing``: The configuration file for Voice Activity Detection
* ``--feature-extraction``: The configuration file for feature extraction
* ``--tool-chain``: The configuration file for the speaker verification tool chain

If you are not at Idiap, please precise the TEMP and USER directories:

* ``--temp-directory``: This typically contains the features, the UBM model, the client models, etc.
* ``--user-directory``: This will contain the output scores (in text format)

If you want to run the experiments in the GRID at Idiap or any equivalent SGE, you can simply specify:

* ``--grid``: The configuration file for the grid setup.

For several datasets, feature types, recognition algorithms, and grid requirements the `SPEAR`_ provides these configuration files.
They are located in the *config/...* directories.
It is also safe to design one experiment and re-use one configuration file for all options as long as the configuration file includes all desired information:

* The database: ``name, db, protocol; wav_input_dir, wav_input_ext``;
* The preprocessing: ``preprocessor = spkrec.preprocessing.<PREPROCESSOR>``;
* The feature extraction: ``extractor = spkrec.feature_extraction.<EXTRACTOR>``;
* The tool: ``tool = spkrec.tools.<TOOL>``; plus configurations of the tool itself
* Grid parameters: They help to configure which queues are used for each of the steps, how much files per job, etc.

If no grid configuration file is specified, the experiment is run sequentially on the local machine with a single core.

If you want to run on a local machine with multiple cores, you have to precise the grid type in your configuration file:

* ``grid_type='local'``

Then run your script with the new configuration file and excute the following command line after precising the number of parallel jobs to be used (e.g. 8)::

   $ bin/jman --local -vv run-scheduler --parallel 8

By default, the ZT score normalization is activated. To deactivate it, please add the ``-z`` to the command line.


III- Experiment design
-----------------------

To be very flexible, the tool chains in the `SPEAR`_ are designed in several stages including::

  1. Preprocessing (Voice Activity Detection)
  2  Feature Extraction
  3. UBM Training and Projection (computation of sufficient statistics)
  4. Subspace Training and Projection (for ISV, JFA and I-Vector modeling)
  5. Conditioning and Compensation (for I-Vector modeling)
  6. Client Model Enrollment
  7. Scoring and score normalization

Note that not all tools implement all of the stages.

1. Voice Activity Detection
~~~~~~~~~~~~~~~~~~~~~~~~~~~
This step aims to filter out the non speech part. Depending on the configuration file, several routines can be enabled or disabled.

* Energy-based VAD
* 4Hz Modulation energy based VAD

2. Feature Extraction
~~~~~~~~~~~~~~~~~~~~~
This step aims to extract features. Depending on the configuration file, several routines can be enabled or disabled.

* LFCC/MFCC feature extraction
* Spectrogram extraction
* Feature normalization
* `HTK`_ Feature reader
* `SPro`_ Feature reader

3. Universal Background Model Training and Projection
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This step aims at computing the universal background model referenced as `Projector`. The training includes both k-means and ML steps. In the parallel implementation, the E (Estimation) step is split to run on parallel processes.
Then, the computation of sufficient statistics in `SPEAR`_ is referenced as the **projection-ubm** step.
It aims at projecting the cepstral features using the previously trained Projector.

4. Subspace Training and Projection
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This steps aims at estimating the subspaces needed by ISV, JFA and I-Vector. The I-Vector can also be parallelized similarly to the UBM. The projection here is referenced by either `projection-isv`, `projection-jfa`, or `projection-ivector`. Notice that the I-Vector projection process is the extraction of the i-vectors.

5. Conditioning and Compensation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This steps is used by the I-Vector toolchain. It includes Whitening, Length Normalization, LDA and WCCN projection.

6. Model Enrollment
~~~~~~~~~~~~~~~~~~~
Model enrollment defines the stage, where several (projected or compensated) features of one identity are used to enroll the model for that identity.
In the easiest case, the features are simply averaged, and the average feature is used as a model.

7. Scoring
~~~~~~~~~~
In the final scoring stage, the models are compared to probe features and a similarity score is computed for each pair of model and probe.
Some of the models (the so-called T-Norm-Model) and some of the probe features (so-called Z-Norm-probe-features) are split up, so they can be used to normalize the scores later on.

In addition, there are independent scripts for fusion and evaluation.

8. Fusion
~~~~~~~~~
The fusion of scores from different systems is done using `logistic regression`_ that should be trained normally on the development scores.

9. Evaluation
~~~~~~~~~~~~~
One way to compute the final result is to use the *bin/evaluate.py* e.g., by calling::

  $ bin/evaluate.py -d PATH/TO/USER/DIRECTORY/scores-dev -e PATH/TO/USER/DIRECTORY/scores-eval -c EER -D DET.pdf -x

This will compute the EER, the minCLLR, CLLR, and draw the DET curve. To better compare different systems using DET curves, a separate script can be used like in this example::

  $ ./bin/det.py -s gmm-scores isv-scores ivector-scores -n GMM ISV i-vectors


IV- Command line options
------------------------

Additionally to some of the required command line options discussed above, there are several options to modify the behavior of the `SPEAR`_ experiments.
One set of command line options change the directory structure of the output:

* ``--temp-directory``: Base directory where to write temporary files into (the default is */idiap/temp/$USER/<DATABASE>* when using the grid or */scratch/$USER/<DATABASE>* when executing jobs locally)
* ``--user-directory``: Base directory where to write the results, default is */idiap/user/$USER/<DATABASE>*
* ``--sub-directory``: sub-directory into *<TEMP_DIR>* and *<USER_DIR>* where the files generated by the experiment will be put
* ``--score-sub-directory``: name of the sub-directory in *<USER_DIR>/<PROTOCOL>* where the scores are put into

If you want to re-use parts previous experiments, you can specify the directories (which are relative to the *<TEMP_DIR>*, but you can also specify absolute paths), like, e.g.:

* ``--features-directory``

For that purpose, it is also useful to skip parts of the tool chain.
To do that you can use, for e.g.:

* ``--skip-preprocessing``
* ``--skip-feature-extraction``
* ``--skip-projection-training``
* ``--skip-projection-ubm``
* ``--skip-enroler-training``
* ``--skip-model-enrolment``
* ``--skip-score-computation``
* ``--skip-concatenation``

Check the complete list using the `help` option.
although by default files that already exist are not re-created.
To enforce the re-creation of the files, you can use the ``--force`` option, which of course can be combined with the ``--skip...``-options (in which case the skip is preferred).

There are some more command line options that can be specified:

* ``--no-zt-norm``: Disables the computation of the ZT-Norm scores.
* ``--groups``: Enabled to limit the computation to the development ('dev') or test ('eval') group. By default, both groups are evaluated.


V- Datasets
------------

For the moment, there are 4 databases that are tested in `SPEAR`_. Their protocols are also shipped with the tool.

In this README, we give examples of different toolchains applied on different databases: Voxforge, BANCA, TIMIT, MOBIO, and NIST SRE 2012.

1. Voxforge dataset
~~~~~~~~~~~~~~~~~~~
`Voxforge`_ is a free database used in free speech recognition engines. We randomly selected a small part of the english corpus (< 1GB).  It is used as a toy example for our speaker recognition tool since experiment can be easily run on a local machine, and the results can be obtained in a reasonnable amount of time (< 2h).

Unlike TIMIT and BANCA, this dataset is completely free of charge.

More details about how to download the audio files used in our experiments, and how the data is split into Training, Development and Evaluation set can be found here::

  https://pypi.python.org/pypi/bob.db.voxforge

One example of command line is::

  $ bin/verify.py  -d voxforge -p energy_2gauss -e mfcc_60 -a gmm_256g -s ubm_gmm --groups {dev,eval}


In this example, we used the following configuration:

* Energy-based VAD,
* (19 MFCC features + Energy) + First and second derivatives,
* **UBM-GMM** Modelling (with 256 Gaussians), the scoring is done using the linear approximation of the LLR.

The performance of the system on DEV and EVAL are:

* ``DEV: EER = 2.00%``
* ``EVAL: HTER = 1.46%``

If you want to run the same experiment on SGE::

  $ bin/verify.py  -d voxforge -p energy_2gauss -e mfcc_60 -a gmm_256g -s ubm_gmm --groups {dev,eval}  -g grid


If you want to run the parallel implementation of the UBM on the SGE::

  $ ./bin/para_ubm_spkverif_gmm.py -d config/database/voxforge.py -p config/preprocessing/energy.py \
    -f config/features/mfcc_60.py -t config/tools/ubm_gmm/ubm_gmm_256G.py -b ubm_gmm -z \
    --user-directory PATH/TO/USER/DIR --temp-directory PATH/TO/TEMP/DIR -g config/grid/para_training_sge.py


If you want to run the parallel implementation of the UBM on your local machine::

  $ ./bin/para_ubm_spkverif_gmm.py -d config/database/voxforge.py -p config/preprocessing/energy.py \
    -f config/features/mfcc_60.py -t config/tools/ubm_gmm/ubm_gmm_256G.py -b ubm_gmm -z \
    --user-directory PATH/TO/USER/DIR --temp-directory PATH/TO/TEMP/DIR -g config/grid/para_training_local.py

$ bin/jman --local -vv run-scheduler --parallel 6

In this example, the number of nodes is 6.

Another example is to use **ISV** toolchain instead of UBM-GMM::

  $ ./bin/spkverif_isv.py -d config/database/voxforge.py -p config/preprocessing/energy.py \
   -f config/features/mfcc_60.py -t config/tools/isv/isv_256g_u50.py  -z -b isv \
   --user-directory PATH/TO/USER/DIR --temp-directory PATH/TO/TEMP/DIR

* ``DEV: EER = 1.67%``
* ``EVAL: HTER = 1.28%``

One can also try **JFA** toolchain::

  $ ./bin/spkverif_jfa.py -d config/database/voxforge.py -p config/preprocessing/energy.py \
   -f config/features/mfcc_60.py -t config/tools/jfa/jfa_256_v5_u10.py  -z -b jfa \
   --user-directory PATH/TO/USER/DIR --temp-directory PATH/TO/TEMP/DIR

* ``DEV: EER = 4.33%``
* ``EVAL: HTER = 5.89%``

or also **IVector** toolchain where **Whitening, L-Norm, LDA, WCCN** are used like in this example where the score computation is done using **Cosine distance**::

  $ ./bin/spkverif_ivector.py -d config/database/voxforge.py -p config/preprocessing/energy.py \
   -f config/features/mfcc_60.py -t config/tools/ivec/ivec_256g_t100_cosine.py -z -b ivector_cosine \
   --user-directory PATH/TO/USER/DIR --temp-directory PATH/TO/TEMP/DIR

* ``DEV: EER = 15.33%``
* ``EVAL: HTER = 15.78%``

The scoring computation can also be done using **PLDA**::

  $ ./bin/spkverif_ivector.py -d config/database/voxforge.py -p config/preprocessing/energy.py \
   -f config/features/mfcc_60.py -t config/tools/ivec/ivec_256g_t100_plda.py -z -b ivector_plda \
   --user-directory PATH/TO/USER/DIR --temp-directory PATH/TO/TEMP/DIR

* ``DEV: EER = 15.33%``
* ``EVAL: HTER = 16.93%``


Note that in the previous examples, our goal is not to optimize the parameters on the DEV set but to provide examples of use.

2. BANCA dataset
~~~~~~~~~~~~~~~~
`BANCA`_ is a simple bimodal database with relatively clean data. The results are already very good with a simple baseline UBM-GMM system. An example of use can be::

  $ bin/spkverif_gmm.py -d config/database/banca_audio_G.py -p config/preprocessing/energy.py \
    -f config/features/mfcc_60.py -t config/tools/ubm_gmm/ubm_gmm_256G_regular_scoring.py \
    --user-directory PATH/TO/USER/DIR --temp-directory PATH/TO/TEMP/DIR -z

The configuration in this example is similar to the previous one with the only difference of using the regular LLR instead of its linear approximation.

Here is the performance of this system:

* ``DEV: EER = 1.66%``
* ``EVAL: EER = 0.69%``


3. TIMIT dataset
~~~~~~~~~~~~~~~~
`TIMIT`_ is one of the oldest databases (year 1993) used to evaluate speaker recognition systems. In the following example, the processing is done on the development set, and LFCC features are used::

  $ ./bin/spkverif_gmm.py -d config/database/timit.py -p config/preprocessing/energy.py \
    -f config/features/lfcc_60.py -t config/tools/ubm_gmm/ubm_gmm_256G.py \
    --user-directory PATH/TO/USER/DIR --temp-directory PATH/TO/TEMP/DIR -b lfcc -z --groups dev

Here is the performance of the system on the Development set:

* ``DEV: EER = 2.68%``


4. MOBIO dataset
~~~~~~~~~~~~~~~~
This is a more challenging database. The noise and the short duration of the segments make the task of speaker recognition relatively difficult. The following experiment on male group (Mobile-0) uses the 4Hz modulation energy based VAD, and the ISV (with dimU=50) modelling technique::

  $ ./bin/spkverif_isv.py -d config/database/mobio/mobile0-male.py -p config/preprocessing/mod_4hz.py \
   -f config/features/mfcc_60.py -t config/tools/isv/isv_u50.py \
   --user-directory PATH/TO/USER/DIR --temp-directory PATH/TO/TEMP/DIR -z

Here is the performance of this system:

* ``DEV: EER = 10.40%``
* ``EVAL: EER = 10.36%``

To generate the results presented in the ICASSP 2014 paper, please check the script included in the `icassp` folder of the toolbox.
Note that the MOBIO dataset has different protocols, and that are all implemented in `bob.db.mobio`_. But in this toolbox, we provide separately mobile-0 protocol (into filelist format) for simplicity.

5. NIST SRE 2012
~~~~~~~~~~~~~~~~
We first invite you to read the paper describing our system submitted to the NIST SRE 2012 Evaluation. The protocols on the development set are the results of a joint work by the I4U group. To reproduce the results, please check this dedicated package::

  https://pypi.python.org/pypi/spear.nist_sre12

.. note::
  For any additional information, please use our mailing list::
  https://groups.google.com/forum/#!forum/bob-devel



Documentation
-------------

References
-----------

.. [Reynolds2000] *Reynolds, Douglas A., Thomas F. Quatieri, and Robert B. Dunn*. **Speaker Verification Using Adapted Gaussian Mixture Models**, Digital signal processing 10.1 (2000): 19-41.
.. [Vogt2008]   *R. Vogt, S. Sridharan*. **'Explicit Modelling of Session Variability for Speaker Verification'**, Computer Speech & Language, 2008, vol. 22, no. 1, pp. 17-38
.. [McCool2013] *C. McCool, R. Wallace, M. McLaren, L. El Shafey, S. Marcel*. **'Session Variability Modelling for Face Authentication'**, IET Biometrics, 2013
.. [Dehak2010] *N. Dehak, P. Kenny, R. Dehak, P. Dumouchel, P. Ouellet*, **'Front End Factor Analysis for Speaker Verification'**, IEEE Transactions on Audio, Speech and Language Processing, 2010, vol. 19, issue 4, pp. 788-798
.. [ElShafey2014] *Laurent El Shafey, Chris McCool, Roy Wallace, Sebastien Marcel*. **'A Scalable Formulation of Probabilistic Linear Discriminant Analysis: Applied to Face Recognition'**, TPAMI'2014
.. [PrinceElder2007] *Prince and Elder*. **'Probabilistic Linear Discriminant Analysis for Inference About Identity'**, ICCV'2007
.. [LiFu2012] *Li, Fu, Mohammed, Elder and Prince*. **'Probabilistic Models for Inference about Identity'**,  TPAMI'2012
.. [WikiEM] `Expectation Maximization <http://en.wikipedia.org/wiki/Expectation%E2%80%93maximization_algorithm>`_



.. _Bob: http://www.idiap.ch/software/bob
.. _local.bob.recipe: https://github.com/idiap/local.bob.recipe
.. _gridtk: https://pypi.python.org/pypi/gridtk
.. _BuildOut: http://www.buildout.org/
.. _NIST: http://www.nist.gov/itl/iad/ig/focs.cfm
.. _bob.db.verification.filelist: https://pypi.python.org/pypi/bob.db.verification.filelist
.. _bob.sox: https://pypi.python.org/pypi/bob.sox
.. _spear: https://pypi.python.org/pypi/bob.spear
.. _pypi: https://pypi.python.org/pypi
.. _Voxforge: http://www.voxforge.org/
.. _BANCA: http://www.ee.surrey.ac.uk/CVSSP/banca/
.. _TIMIT: http://www.ldc.upenn.edu/Catalog/catalogEntry.jsp?catalogId=LDC93S1
.. _logistic regression: http://en.wikipedia.org/wiki/Logistic_regression
.. _Spro: https://gforge.inria.fr/projects/spro
.. _HTK: http://htk.eng.cam.ac.uk/
.. _bob.db.mobio: https://pypi.python.org/pypi/bob.db.mobio
