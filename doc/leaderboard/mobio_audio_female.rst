.. author: Yannick Dayer <yannick.dayer@idiap.ch>
.. date: Mon 09 May 2022 13:48:48 UTC+02


.. _bob.bio.spear.mobio-audio-female:

================================
 Mobio Dataset, female subjects
================================

GMM
---

On 128\ [#nodes]_ CPU nodes on the SGE Grid: TODO

.. table:: [Min. criterion: EER] Threshold on Development set: TODO

    =====================  ================  ==================
    ..                     Development       Evaluation
    =====================  ================  ==================

Command used to generate scores::

    $ bob bio pipeline -d mobio-audio-female gmm-mobio -g dev -g eval -l sge

ISV
---

On 128\ [#nodes]_ CPU nodes on the SGE Grid: TODO

.. table:: [Min. criterion: EER] Threshold on Development set: TODO

    =====================  ================  ==================
    ..                     Development       Evaluation
    =====================  ================  ==================

Command used to generate scores::

    $ bob bio pipeline -d mobio-audio-female -p isv-voxforge -g dev -g eval -l sge

Speechbrain ECAPA-TDNN
----------------------

On 128\ [#nodes]_ CPU nodes on the SGE Grid: 12 minutes.

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


Command used to generate scores::

    $ bob bio pipeline -d mobio-audio-female -p speechbrain-ecapa-voxceleb -g dev -g eval -l sge


.. rubric:: Footnotes

.. [#nodes] The number of nodes is a requested maximum amount and can vary depending on
    the number of jobs currently running on the grid as well as the scheduler's load
    estimation. The execution time can then also vary.
