
======================
Implementation Details
======================
To be very flexible, the tool chains are designed in several stages including::

  1. Annotations (Voice Activity Detection)
  2. Feature Extraction
  3. UBM Training and Projection (computation of sufficient statistics)
  4. Subspace Training and Projection (for ISV and I-Vector modeling)
  5. Conditioning and Compensation (for I-Vector modeling)
  6. Client Model Enrollment
  7. Scoring and score normalization

Note that not all tools implement all of the stages.

1. Voice Activity Detection
~~~~~~~~~~~~~~~~~~~~~~~~~~~
This step aims to filter out the non speech part. Depending on the configuration file,
several routines can be enabled or disabled.
The annotator reads the sound data and produces a boolean mask array indicating if
there is voice or not at each audio sample

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

3. Universal Background Model Training
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This step aims at computing the universal background model referenced as `Projector`. The training includes both k-means and ML steps. In the parallel implementation, the E (Estimation) step is split to run on parallel processes.

4. Subspace Training
~~~~~~~~~~~~~~~~~~~~~~
This steps aims at estimating the subspaces needed by ISV, JFA and I-Vector. The I-Vector can also be parallelized similarly to the UBM. For design convenience, the `Projector` and `Enroller` are put together in one HDF5 file.


5. Conditioning and Compensation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This steps is used by the I-Vector toolchain. It includes Whitening, Length Normalization, LDA and WCCN projection. The trained machines are appended to the same HDF5 of `Projector`.

6. Projection
~~~~~~~~~~~~~~
It aims at projecting the cepstral features using the previously trained Projector.

6. Model Enrollment
~~~~~~~~~~~~~~~~~~~~~~~
Model enrollment defines the stage, where several (projected or compensated) features of one identity are used to enroll the model for that identity.
In the easiest case, the features are simply averaged, and the average feature is used as a model.

7. Scoring
~~~~~~~~~~
In the final scoring stage, the models are compared to probe features and a similarity score is computed for each pair of model and probe.
Some of the models (the so-called T-Norm-Model) and some of the probe features (so-called Z-Norm-probe-features) are split up, so they can be used to normalize the scores later on.

8. Fusion
~~~~~~~~~
The fusion of scores from different systems is done using `logistic regression`_ that should be trained normally on the development scores.

9. Evaluation
~~~~~~~~~~~~~
One way to compute the final result is to use ``bob bio evaluate`` e.g., by calling::

  bob bio evaluate --eval PATH/TO/USER/DIRECTORY/scores-dev PATH/TO/USER/DIRECTORY/scores-eval --criterion EER --output results.pdf

This will compute the EER, the minCLLR, CLLR, and draw the DET curve.
To better compare different systems using DET curves, a separate command can be used::

  bob bio det --split gmm-scores.csv isv-scores.csv ivector-scores.csv --titles "GMM,ISV,i-vectors"


.. include:: links.rst
