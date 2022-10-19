.. author: Yannick Dayer <yannick.dayer@idiap.ch>
.. date: Mon 09 May 2022 13:48:48 UTC+02


.. _bob.bio.spear.mobio-audio-male:

==============================
 Mobio Dataset, male subjects
==============================

Dataset Description
-------------------

Mobio is a collection of English voice recordings. The set of male subjects contains:

+--------------------+------------+--------------+
|                    | Identities | Sample count |
+--------------------+------------+--------------+
| train              | 37         | 7104         |
+-------+------------+------------+--------------+
|       | references |            | 120          |
|       +------------+            +--------------+
| dev   | probes     | 24         | 2520         |
+-------+------------+------------+--------------+
|       | references |            | 190          |
|       +------------+            +--------------+
| eval  | probes     | 38         | 3990         |
+-------+------------+------------+--------------+

GMM
---

To run the baseline, use the following command::

    bob bio pipeline simple -d mobio-audio-male gmm-mobio -g dev -g eval -l sge -o results/gmm_mobio_male

Then, to generate the scores, use::

    bob bio metrics -e ./results/gmm_mobio_male/scores-{dev,eval}.csv


.. table:: [Min. criterion: EER] Threshold on Development set: 6.918534e-01

    =====================  ===================  ==================
    ..                     Development          Evaluation
    =====================  ===================  ==================
    Failure to Acquire     0.0%                 0.0%
    False Match Rate       18.3% (10603/57960)  3.2% (4684/147630)
    False Non Match Rate   18.3% (461/2520)     30.4% (1211/3990)
    False Accept Rate      18.3%                3.2%
    False Reject Rate      18.3%                30.4%
    Half Total Error Rate  18.3%                16.8%
    =====================  ===================  ==================

On 128\ [#nodes]_ CPU nodes on the SGE Grid: Ran in 39 minutes (30 minutes of training).

ISV
---

To run the baseline, use the following command::

    bob bio pipeline simple -d mobio-audio-male -p isv-default -g dev -g eval -l sge -o results/isv_mobio_male

Then, to generate the scores, use::

    bob bio metrics -e ./results/isv_mobio_male/scores-{dev,eval}.csv


.. table:: [Min. criterion: EER] Threshold on Development set: 2.974263e-01

    =====================  ==================  ====================
    ..                     Development         Evaluation
    =====================  ==================  ====================
    Failure to Acquire     0.0%                0.0%
    False Match Rate       12.7% (7360/57960)  14.7% (21697/147630)
    False Non Match Rate   12.7% (320/2520)    14.3% (572/3990)
    False Accept Rate      12.7%               14.7%
    False Reject Rate      12.7%               14.3%
    Half Total Error Rate  12.7%               14.5%
    =====================  ==================  ====================

On 128\ [#nodes]_ CPU nodes on the SGE Grid: Ran in 18 minutes (11 minutes of training).

Speechbrain ECAPA-TDNN
----------------------

To run the baseline, use the following command::

    bob bio pipeline simple -d mobio-audio-male -p speechbrain-ecapa-voxceleb -g dev -g eval -l sge -o results/speechbrain_mobio_male

Then, to generate the scores, use::

    bob bio metrics -e ./results/speechbrain_mobio_male/scores-{dev,eval}.csv


.. table:: [Min. criterion: EER] Threshold on Development set: -5.583622e-01

    =====================  ================  ==================
    ..                     Development       Evaluation
    =====================  ================  ==================
    Failure to Acquire     0.0%              0.0%
    False Match Rate       1.4% (828/57960)  3.1% (4620/147630)
    False Non Match Rate   1.4% (36/2520)    1.1% (45/3990)
    False Accept Rate      1.4%              3.1%
    False Reject Rate      1.4%              1.1%
    Half Total Error Rate  1.4%              2.1%
    =====================  ================  ==================

On 128\ [#nodes]_ CPU nodes on the SGE Grid: 19 minutes (no training).


.. rubric:: Footnotes

.. [#nodes] The number of nodes is a requested maximum amount and can vary depending on
    the number of jobs currently running on the grid as well as the scheduler's load
    estimation. The execution time can then also vary.

.. include:: ../links.rst
