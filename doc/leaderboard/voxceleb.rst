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



ISV
---



Speechbrain ECAPA-TDNN
----------------------


.. table:: [Min. criterion: EER ] Threshold on Development set: -7.288057e-01

    =====================  ================
    ..                     Development
    =====================  ================
    Failure to Acquire     0.0%
    False Match Rate       1.0% (189/18860)
    False Non Match Rate   1.0% (189/18860)
    False Accept Rate      1.0%
    False Reject Rate      1.0%
    Half Total Error Rate  1.0%
    =====================  ================

Command used::

    $ bob bio pipeline -d voxceleb -p speechbrain-ecapa-voxceleb -g dev -l sge-demanding -o results/speechbrain_voxceleb

On 128\ [#nodes]_ CPU nodes on the SGE Grid: Ran in 3 minutes (no training).


.. rubric:: Footnotes

.. [#nodes] The number of nodes is a requested maximum amount and can vary depending on
    the number of jobs currently running on the grid as well as the scheduler's load
    estimation. The execution time can then also vary.
