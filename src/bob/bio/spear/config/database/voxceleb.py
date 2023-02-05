#!/usr/bin/env python
# @author: Yannick Dayer <yannick.dayer@idiap.ch>
# @date: Fri 24 Jun 2022 17:55:05 UTC+02

"""VoxCeleb CSV database interface default configuration"""

from bob.bio.spear.database import VoxcelebDatabase

database = VoxcelebDatabase(protocol="voxceleb1")
