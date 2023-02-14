#!/usr/bin/env python
"""Configuration for the Voice Activity Detection (VAD) annotator Energy 2Gauss

This annotator returns a mask (boolean array) of an audio signal, with ones where a
voice is detected, and zeroes otherwise.

Uses 2 Gaussian-modeled Energy.

Usage
-----

Feed this file (also defined as a ``energy-2gauss`` resource) to ``bob bio annotate`` as
configuration::

    $ bob bio annotate -a energy-2gauss -d <database> -o annotations/

or include it in a pipeline.
"""

from bob.bio.spear.annotator import Energy_2Gauss

annotator = Energy_2Gauss()
