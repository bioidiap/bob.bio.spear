.. author: Yannick Dayer <yannick.dayer@idiap.ch>
.. date: Thu 14 Jul 2022 18:50:30 UTC+02


.. _bob.bio.spear.leaderboard.voxceleb:

==================
 VoxCeleb Dataset
==================

Dataset Description
-------------------

VoxCeleb is a collection of voice recording of celebrities extracted from various
Youtube videos.
It contains:

+--------------------+------------+--------------+
|                    | Identities | Sample count |
+--------------------+------------+--------------+
| train              | 1211       | 148642       |
+-------+------------+------------+--------------+
| dev   | references |            | 4874         |
| /     +------------+            +--------------+
| eval  | probes     | 40         | 37720        |
+-------+------------+------------+--------------+

GMM
---

To run the baseline, use the following command::

    $ bob bio pipeline simple -d voxceleb gmm-mobio -l sge-demanding -o results/gmm_voxceleb -n 512

Then, to generate the scores, use::

    $ bob bio metrics -e ./results/gmm_voxceleb/scores-{dev,eval}.csv

.. table:: [Min. criterion: EER ] Threshold on Development set: 1.062216e-01

    =====================  ==================
    ..                     Development
    =====================  ==================
    Failure to Acquire     0.0%
    False Match Rate       18.8% (3538/18860)
    False Non Match Rate   18.8% (3538/18860)
    False Accept Rate      18.8%
    False Reject Rate      18.8%
    Half Total Error Rate  18.8%
    =====================  ==================

On 128\ [#nodes]_ CPU nodes on the SGE Grid: Ran in 10 hours.

ISV
---

TODO


Speechbrain ECAPA-TDNN
----------------------

This baseline reproduces the (speechbrain_). The original paper's reference is the following:

    @inproceedings{DBLP:conf/interspeech/DesplanquesTD20,
      author    = {Brecht Desplanques and
                   Jenthe Thienpondt and
                   Kris Demuynck},
      editor    = {Helen Meng and
                   Bo Xu and
                   Thomas Fang Zheng},
      title     = {{ECAPA-TDNN:} Emphasized Channel Attention, Propagation and Aggregation
                   in {TDNN} Based Speaker Verification},
      booktitle = {Interspeech 2020},
      pages     = {3830--3834},
      publisher = {{ISCA}},
      year      = {2020},
    }

To run the baseline, use the following command::

    $ bob bio pipeline simple -vvv -d voxceleb -p speechbrain-ecapa-voxceleb -g dev -g eval -o ./results/speechbrain_voxceleb

Then, to generate the scores, use::

    $ bob bio metrics -e ./results/speechbrain_voxceleb/scores-{dev,eval}.csv

.. table:: [Min. criterion: EER] Threshold on Development set: -6.159925e-01

    =====================  ================  ================
    ..                     Development       Evaluation
    =====================  ================  ================
    Failure to Acquire     0.0%              0.0%
    False Match Rate       1.0% (189/18860)  1.0% (189/18860)
    False Non Match Rate   1.0% (189/18860)  1.0% (189/18860)
    False Accept Rate      1.0%              1.0%
    False Reject Rate      1.0%              1.0%
    Half Total Error Rate  1.0%              1.0%
    =====================  ================  ================

On 128\ [#nodes]_ CPU nodes on the SGE Grid: Ran in 9 minutes (no training).



.. note::

    ECAPA-TDNN gives a reference result of 0.8% EER on VoxCeleb. However, they were
    using a customized version of the dataset (``VoxCeleb (cleaned)``) which ignores
    109 probe files (presumably containing wrong data) from our own dataset.


.. rubric:: Footnotes

.. [#nodes] The number of nodes is a requested maximum amount and can vary depending on
    the number of jobs currently running on the grid as well as the scheduler's load
    estimation. The execution time can then also vary.
