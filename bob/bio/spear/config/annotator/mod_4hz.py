#!/usr/bin/env python
"""Configuration for the Voice Activity Detection (VAD) annotator Mod-4hz

This annotator returns a mask (boolean array) of an audio signal, with ones where a
voice is detected, and zeroes otherwise.

Uses 4Hz modulation energy

Usage
-----

Feed this file (also defined as a ``mod-4hz`` resource) to ``bob bio annotate`` as
configuration::

    $ bob bio annotate -a mod-4hz -d <database> -o annotations/

or include it in a pipeline.
"""

from bob.bio.spear.annotator import Mod_4Hz

annotator = Mod_4Hz()
