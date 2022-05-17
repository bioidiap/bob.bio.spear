.. author: Yannick Dayer <yannick.dayer@idiap.ch>
.. date: Mon 09 May 2022 13:48:48 UTC+02

.. _bob.bio.spear.leaderboard.nist-sre04-16:

=======================
 NIST-SRE04-16 Dataset
=======================

GMM
---

On 128\ [#nodes]_ CPU nodes on the SGE Grid: TODO

.. table:: [Min. criterion: EER] Threshold on Development set: TODO

    =====================  ================  ==================
    ..                     Development       Evaluation
    =====================  ================  ==================

Command used::

    $ bob bio pipeline -d nist-sre04to16 -p gmm-nist -g dev -g eval -l sge

ISV
---

On 128\ [#nodes]_ CPU nodes on the SGE Grid: TODO

.. table:: [Min. criterion: EER] Threshold on Development set: TODO

    =====================  ================  ==================
    ..                     Development       Evaluation
    =====================  ================  ==================

Command used::

    $ bob bio pipeline -d nist-sre04to16 -p isv-nist -g dev -g eval -l sge

Speechbrain ECAPA-TDNN
----------------------

On 128\ [#nodes]_ CPU nodes on the SGE Grid: TODO

.. table:: [Min. criterion: EER] Threshold on Development set: TODO

    =====================  ================  ==================
    ..                     Development       Evaluation
    =====================  ================  ==================

Command used::

    $ bob bio pipeline -d nist-sre04to16 -p speechbrain-ecapa-voxceleb -g dev -g eval -l sge


.. rubric:: Footnotes

.. [#nodes] The number of nodes is a requested maximum amount and can vary depending on
    the number of jobs currently running on the grid as well as the scheduler's load
    estimation. The execution time can then also vary.
