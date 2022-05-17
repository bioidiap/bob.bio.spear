.. author: Yannick Dayer <yannick.dayer@idiap.ch>
.. date: Mon 09 May 2022 13:48:48 UTC+02


.. _bob.bio.spear.mobio-audio-male:

==============================
 Mobio Dataset, male subjects
==============================

GMM
---

On 128\ [#nodes]_ CPU nodes on the SGE Grid: TODO

.. table:: [Min. criterion: EER] Threshold on Development set: TODO

    =====================  ================  ==================
    ..                     Development       Evaluation
    =====================  ================  ==================

Command used to generate scores::

    $ bob bio pipeline -d mobio-audio-male gmm-mobio -g dev -g eval -l sge

ISV
---

On 128\ [#nodes]_ CPU nodes on the SGE Grid: TODO

.. table:: [Min. criterion: EER] Threshold on Development set: TODO

    =====================  ================  ==================
    ..                     Development       Evaluation
    =====================  ================  ==================

Command used to generate scores::

    $ bob bio pipeline -d mobio-audio-male -p isv-voxforge -g dev -g eval -l sge

Speechbrain ECAPA-TDNN
----------------------

On 128\ [#nodes]_ CPU nodes on the SGE Grid: 19 minutes (no training).

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


Command used to generate scores::

    $ bob bio pipeline -d mobio-audio-male -p speechbrain-ecapa-voxceleb -g dev -g eval -l sge


.. rubric:: Footnotes

.. [#nodes] The number of nodes is a requested maximum amount and can vary depending on
    the number of jobs currently running on the grid as well as the scheduler's load
    estimation. The execution time can then also vary.
