#!/usr/bin/env python
"""Configuration for the Voice Activity Detection (VAD) annotator Energy_Thr

This annotator returns a mask (boolean array) of an audio signal, with ones where a
voice is detected, and zeroes otherwise.

Uses energy threshold

Usage
-----

Feed this file (also defined as a ``energy-thr`` resource) to ``bob bio annotate`` as
configuration::

    $ bob bio annotate -a energy-thr -d <database> -o annotations/

or include it in a pipeline::

    $ bob bio pipeline simple energy-thr
"""

from bob.bio.spear.annotator import Energy_Thr

annotator = Energy_Thr()
