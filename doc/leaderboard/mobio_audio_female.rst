.. author: Yannick Dayer <yannick.dayer@idiap.ch>
.. date: Mon 09 May 2022 13:48:48 UTC+02


.. _bob.bio.spear.mobio-audio-female:

================================
 Mobio Dataset, female subjects
================================

Dataset Description
-------------------

Mobio is a collection of English voice recordings. The set of female subjects contains:

+--------------------+------------+--------------+
|                    | Identities | Sample count |
+--------------------+------------+--------------+
| train              | 13         | 2406         |
+-------+------------+------------+--------------+
|       | references |            | 90           |
|       +------------+            +--------------+
| dev   | probes     | 18         | 1890         |
+-------+------------+------------+--------------+
|       | references |            | 100          |
|       +------------+            +--------------+
| eval  | probes     | 20         | 2100         |
+-------+------------+------------+--------------+

GMM
---

To run the baseline, use the following command::

    bob bio pipeline simple -d mobio-audio-female gmm-mobio -g dev -g eval -l sge -o results/gmm_mobio_female

Then, to generate the scores, use::

    bob bio metrics -e ./results/gmm_mobio_female/scores-{dev,eval}.csv

.. table:: [Min. criterion: EER] Threshold on Development set: 7.550647e-01

    =====================  ==================  =================
    ..                     Development         Evaluation
    =====================  ==================  =================
    Failure to Acquire     0.0%                0.0%
    False Match Rate       20.6% (6632/32130)  7.8% (3093/39900)
    False Non Match Rate   20.6% (390/1890)    26.8% (562/2100)
    False Accept Rate      20.6%               7.8%
    False Reject Rate      20.6%               26.8%
    Half Total Error Rate  20.6%               17.3%
    =====================  ==================  =================

On 128\ [#nodes]_ CPU nodes on the SGE Grid: Ran in 15 minutes (11 minutes of training).

ISV
---

To run the baseline, use the following command::

    bob bio pipeline simple -d mobio-audio-female -p isv-default -g dev -g eval -l sge -o results/isv_mobio_female

Then, to generate the scores, use::

    bob bio metrics -e ./results/isv_mobio_female/scores-{dev,eval}.csv


.. table:: [Min. criterion: EER] Threshold on Development set: 3.483318e-01

    =====================  ==================  ==================
    ..                     Development         Evaluation
    =====================  ==================  ==================
    Failure to Acquire     0.0%                0.0%
    False Match Rate       14.7% (4710/32130)  20.3% (8103/39900)
    False Non Match Rate   14.7% (277/1890)    17.4% (366/2100)
    False Accept Rate      14.7%               20.3%
    False Reject Rate      14.7%               17.4%
    Half Total Error Rate  14.7%               18.9%
    =====================  ==================  ==================


On 128\ [#nodes]_ CPU nodes on the SGE Grid: Ran in 8 minutes (3 minutes of training).

Speechbrain ECAPA-TDNN
----------------------


To run the baseline, use the following command::

    bob bio pipeline simple -d mobio-audio-female -p speechbrain-ecapa-voxceleb -g dev -g eval -l sge -o results/speechbrain_mobio_female

Then, to generate the scores, use::

    bob bio metrics -e ./results/speechbrain_mobio_female/scores-{dev,eval}.csv


.. table:: [Min. criterion: EER] Threshold on Development set: -5.091601e-01

    =====================  ================  ==================
    ..                     Development       Evaluation
    =====================  ================  ==================
    Failure to Acquire     0.0%              0.0%
    False Match Rate       1.9% (616/32130)  10.8% (4307/39900)
    False Non Match Rate   1.9% (36/1890)    2.5% (52/2100)
    False Accept Rate      1.9%              10.8%
    False Reject Rate      1.9%              2.5%
    Half Total Error Rate  1.9%              6.6%
    =====================  ================  ==================

On 128\ [#nodes]_ CPU nodes on the SGE Grid: 12 minutes (no training).


.. rubric:: Footnotes

.. [#nodes] The number of nodes is a requested maximum amount and can vary depending on
    the number of jobs currently running on the grid as well as the scheduler's load
    estimation. The execution time can then also vary.

.. include:: ../links.rst
