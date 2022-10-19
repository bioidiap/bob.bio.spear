.. author: Yannick Dayer <yannick.dayer@idiap.ch>
.. date: Mon 09 May 2022 13:40:01 UTC+02

=============
 Leaderboard
=============

These pages present the performance of a set of biometric pipelines on various
datasets.

Pipelines description
---------------------

Each pipeline configuration is available in the ``bob/bio/spear/config/pipeline``
folder. Some pipelines configurations are tuned for a specific dataset (e.g.
``gmm-default`` has its ``number_of_gaussians`` parameter adapted to VoxForge).

GMM:
    Consists of a training step to train the GMM UBM, and two biometric experiments
    (*dev* and *eval*).

ISV:
    Consists of a training step to train the GMM UBM and the ISV, and two biometric
    experiments (*dev* and *eval*).

Speechbrain ECAPA-TDNN trained on VoxCeleb:
    Does only the two biometric experiments (as we use a pretrained model).

Metrics generation (score analysis)
-----------------------------------

In the following pages, the metrics tables are generated using the command::

    bob bio metrics -e ./results/scores-{dev,eval}.csv


Leaderboard for each dataset
-----------------------------

.. toctree::
    :maxdepth: 2

    voxforge
    mobio_audio_male
    mobio_audio_female
    nist_sre04_16
    voxceleb

.. include:: ../links.rst
