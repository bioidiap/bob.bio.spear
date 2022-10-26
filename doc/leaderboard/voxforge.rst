.. author: Yannick Dayer <yannick.dayer@idiap.ch>
.. date: Mon 09 May 2022 13:48:48 UTC+02


.. _bob.bio.spear.leaderboard.voxforge:

==================
 VoxForge Dataset
==================

Dataset Description
-------------------

VoxForge is a collection of voice recordings from various languages. The set that we
use in ``bob.bio.spear`` is a part of the English VoxForge corpus. It contains:

+--------------------+------------+--------------+
|                    | Identities | Sample count |
+--------------------+------------+--------------+
| train              | 10         | 3148         |
+-------+------------+------------+--------------+
|       | references |            | 1304         |
|       +------------+            +--------------+
| dev   | probes     | 10         | 300          |
+-------+------------+------------+--------------+
|       | references |            | 1509         |
|       +------------+            +--------------+
| eval  | probes     | 10         | 300          |
+-------+------------+------------+--------------+

GMM
---

To run the baseline, use the following command::

    bob bio pipeline simple -d voxforge -p gmm-default -g dev -g eval -l sge -o results/gmm_voxforge

Then, to generate the scores, use::

    bob bio metrics -e ./results/gmm_voxforge/scores-{dev,eval}.csv

.. table:: [Min. criterion: EER] Threshold on Development set: 2.128360e+00

    =====================  ==============  ==============
    ..                     Development     Evaluation
    =====================  ==============  ==============
    Failure to Acquire     0.0%            0.0%
    False Match Rate       2.0% (54/2700)  1.8% (48/2700)
    False Non Match Rate   2.0% (6/300)    1.3% (4/300)
    False Accept Rate      2.0%            1.8%
    False Reject Rate      2.0%            1.3%
    Half Total Error Rate  2.0%            1.6%
    =====================  ==============  ==============

On 128\ [#nodes]_ CPU nodes on the SGE Grid: Ran in 13 minutes (5 minutes of training).

ISV
---

To run the baseline, use the following command::

    bob bio pipeline simple -d voxforge -p isv-default -g dev -g eval -l sge -o results/isv_voxforge

Then, to generate the scores, use::

    bob bio metrics -e ./results/isv_voxforge/scores-{dev,eval}.csv

.. table:: [Min. criterion: EER] Threshold on Development: 1.680925e+00

    =====================  ==============  ==============
    ..                     Development     Evaluation
    =====================  ==============  ==============
    Failure to Acquire     0.0%            0.0%
    False Match Rate       1.3% (36/2700)  0.7% (20/2700)
    False Non Match Rate   1.3% (4/300)    2.7% (8/300)
    False Accept Rate      1.3%            0.7%
    False Reject Rate      1.3%            2.7%
    Half Total Error Rate  1.3%            1.7%
    =====================  ==============  ==============

On 128\ [#nodes]_ CPU nodes on the SGE Grid: Ran in 13 minutes (7 minutes of training).

I-Vector
--------

To run the baseline, use the following command::

    bob bio pipeline simple -d voxforge -p ivector-default -g dev -g eval -l sge -o results/ivector_voxforge

Then, to generate the scores, use::

    bob bio metrics -e ./results/ivector_voxforge/scores-{dev,eval}.csv

.. table:: [Min. criterion: EER ] Threshold on Development set: -7.924394e-01

    =====================  ===============  ===============
    ..                     Development      Evaluation
    =====================  ===============  ===============
    Failure to Acquire     0.0%             0.0%
    False Match Rate       4.3% (116/2700)  6.9% (186/2700)
    False Non Match Rate   4.3% (13/300)    4.3% (13/300)
    False Accept Rate      4.3%             6.9%
    False Reject Rate      4.3%             4.3%
    Half Total Error Rate  4.3%             5.6%
    =====================  ===============  ===============

I-Vector PLDA
-------------

To run the baseline, use the following command::

    bob bio pipeline simple -d voxforge -p ivector-plda -g dev -g eval -l sge -o results/ivector_plda_voxforge

Then, to generate the scores, use::

    bob bio metrics -e ./results/ivector_plda_voxforge/scores-{dev,eval}.csv

.. TODO

Speechbrain ECAPA-TDNN
----------------------

To run the baseline, use the following command::

    bob bio pipeline simple -d voxforge -p speechbrain-ecapa-voxceleb -g dev -g eval -l sge -o results/speechbrain_voxforge

Then, to generate the scores, use::

    bob bio metrics -e ./results/speechbrain_voxforge/scores-{dev,eval}.csv

.. table:: [Min. criterion: EER] Threshold on Development set: -6.159925e-01

    =====================  =============  ==============
    ..                     Development    Evaluation
    =====================  =============  ==============
    Failure to Acquire     0.0%           0.0%
    False Match Rate       0.0% (0/2700)  0.8% (21/2700)
    False Non Match Rate   0.0% (0/300)   0.0% (0/300)
    False Accept Rate      0.0%           0.8%
    False Reject Rate      0.0%           0.0%
    Half Total Error Rate  0.0%           0.4%
    =====================  =============  ==============

On 128\ [#nodes]_ CPU nodes on the SGE Grid: Ran in 9 minutes (no training).


.. rubric:: Footnotes

.. [#nodes] The number of nodes is a requested maximum amount and can vary depending on
    the number of jobs currently running on the grid as well as the scheduler's load
    estimation. The execution time can then also vary.

.. include:: ../links.rst
