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

.. table:: [Min. criterion: EER] Threshold on Development set: TODO

    =====================  ================  ==================
    ..                     Development       Evaluation
    =====================  ================  ==================

Command used::

    $ bob bio pipeline -d nist-sre04to16 -p gmm-nist -g dev -g eval -l sge -o results/gmm_nist

On 128\ [#nodes]_ CPU nodes on the SGE Grid: TODO

ISV
---

.. table:: [Min. criterion: EER] Threshold on Development set: TODO

    =====================  ================  ==================
    ..                     Development       Evaluation
    =====================  ================  ==================

Command used::

    $ bob bio pipeline -d nist-sre04to16 -p isv-nist -g dev -g eval -l sge -o results/isv_nist

On 128\ [#nodes]_ CPU nodes on the SGE Grid: TODO

Speechbrain ECAPA-TDNN
----------------------

.. table:: [Min. criterion: EER] Threshold on Development set: -2.857224e-01

    =====================  ===================  =======================
    ..                     Development          Evaluation
    =====================  ===================  =======================
    Failure to Acquire     0.0%                 0.0%
    False Match Rate       28.4% (27400/96342)  28.7% (2142253/7453619)
    False Non Match Rate   28.4% (62/218)       33.7% (57/169)
    False Accept Rate      28.4%                28.7%
    False Reject Rate      28.4%                33.7%
    Half Total Error Rate  28.4%                31.2%
    =====================  ===================  =======================

.. todo::

    These results are not taking into account the ``C_ID_X`` unknown identity...

    In the *core* protocol, there are probes with the ``"C_ID_X"`` ``reference_id``.
    These samples do not come from the same person and will be treated as one person by
    the analysis scripts. This is not good. We have to handle them.

Command used::

    $ bob bio pipeline -d nist-sre04to16 -p speechbrain-ecapa-voxceleb -g dev -g eval -l sge -o results/speechbrain_nist

On 128\ [#nodes]_ CPU nodes on the SGE Grid: Ran in 50 minutes (no training).


.. rubric:: Footnotes

.. [#nodes] The number of nodes is a requested maximum amount and can vary depending on
    the number of jobs currently running on the grid as well as the scheduler's load
    estimation. The execution time can then also vary.
