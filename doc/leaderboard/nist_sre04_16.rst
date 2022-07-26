.. author: Yannick Dayer <yannick.dayer@idiap.ch>
.. date: Mon 09 May 2022 13:48:48 UTC+02

.. _bob.bio.spear.leaderboard.nist-sre04-16:

=======================
 NIST-SRE04-16 Dataset
=======================

Dataset Description
-------------------

This is an aggregation of the NIST-SRE datasets from 2004 to 2016.

+--------------------+------------+--------------+
|                    | Identities | Sample count |
+--------------------+------------+--------------+
| train              | 6213       | 71728        |
+-------+------------+------------+--------------+
|       | references | 80         | 120          |
|       +------------+------------+--------------+
| dev   | probes     | 5          | 1207         |
+-------+------------+------------+--------------+
|       | references | 802        | 1202         |
|       +------------+------------+--------------+
| eval  | probes     | 5          | 9294         |
+-------+------------+------------+--------------+

GMM
---

To run the baseline, use the following command::

    $ bob bio pipeline simple -d nist-sre04to16 -p gmm-nist -g dev -g eval -l sge -o results/gmm_nist

Then, to generate the scores, use::

    $ bob bio metrics -e ./results/gmm_nist/scores-{dev,eval}.csv


.. table:: [Min. criterion: EER] Threshold on Development set: TODO

    =====================  ================  ==================
    ..                     Development       Evaluation
    =====================  ================  ==================

On 128\ [#nodes]_ CPU nodes on the SGE Grid: TODO

ISV
---

To run the baseline, use the following command::

    $ bob bio pipeline simple -d nist-sre04to16 -p isv-nist -g dev -g eval -l sge -o results/isv_nist

Then, to generate the scores, use::

    $ bob bio metrics -e ./results/isv_nist/scores-{dev,eval}.csv

.. table:: [Min. criterion: EER] Threshold on Development set: TODO

    =====================  ================  ==================
    ..                     Development       Evaluation
    =====================  ================  ==================

On 128\ [#nodes]_ CPU nodes on the SGE Grid: TODO

Speechbrain ECAPA-TDNN
----------------------

To run the baseline, use the following command::

    $ bob bio pipeline simple -d nist-sre04to16 -p speechbrain-ecapa-voxceleb -g dev -g eval -l sge -o results/speechbrain_nist

Then, to generate the scores, use::

    $ bob bio metrics -e ./results/speechbrain_mobio_male/scores-{dev,eval}.csv


.. table:: [Min. criterion: EER ] Threshold on Development set: -3.860876e-01

    =====================  ===================  ======================
    ..                     Development          Evaluation
    =====================  ===================  ======================
    Failure to Acquire     0.0%                 0.0%
    False Match Rate       12.9% (12434/96342)  11.4% (852522/7453619)
    False Non Match Rate   12.8% (28/218)       23.7% (40/169)
    False Accept Rate      12.9%                11.4%
    False Reject Rate      12.8%                23.7%
    Half Total Error Rate  12.9%                17.6%
    =====================  ===================  ======================

On 70\ [#nodes]_ CPU nodes on the SGE Grid: Ran in 55 minutes (no training).


.. rubric:: Footnotes

.. [#nodes] The number of nodes is a requested maximum amount and can vary depending on
    the number of jobs currently running on the grid as well as the scheduler's load
    estimation. The execution time can then also vary.

.. include:: ../links.rst
