#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# @author: Manuel Guenther <Manuel.Guenther@idiap.ch>
# @date: Thu May 24 10:41:42 CEST 2012
#
# Copyright (C) 2011-2012 Idiap Research Institute, Martigny, Switzerland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from nose.plugins.skip import SkipTest

import bob.bio.base
from bob.bio.base.test.utils import db_available
from bob.bio.base.test.test_database_implementations import check_database, check_database_zt


@db_available('voxforge')
def test_voxforge():
    database = bob.bio.base.load_resource('voxforge', 'database', preferred_package='bob.bio.spear')
    try:
        check_database(database, groups=('dev', 'eval'))
    except IOError as e:
        raise SkipTest(
            "The database could not queried; probably the db.sql3 file is missing. Here is the error: '%s'" % e)

@db_available('mobio')
def test_mobio():
    database = bob.bio.base.load_resource('mobio-audio-male', 'database', preferred_package='bob.bio.spear')
    try:
        check_database_zt(database, models_depend=True)
    except IOError as e:
        raise SkipTest(
            "The database could not queried; probably the db.sql3 file is missing. Here is the error: '%s'" % e)

@db_available('avspoof-licit')
def test_avspoof_licit():
    database = bob.bio.base.load_resource('licit', 'database', preferred_package='bob.bio.spear')
    try:
        check_database(database, groups=('dev', 'eval'), training_depends=True)
    except IOError as e:
        raise SkipTest(
            "The database could not queried; probably the db.sql3 file is missing. Here is the error: '%s'" % e)

@db_available('asvspoof-licit')
def test_asvspoof_licit():
    database = bob.bio.base.load_resource('ASV-female', 'database', preferred_package='bob.bio.spear')
    try:
        check_database(database, groups=('dev', 'eval'), training_depends=True, skip_train=True)
    except IOError as e:
        raise SkipTest(
            "The database could not queried; probably the db.sql3 file is missing. Here is the error: '%s'" % e)

@db_available('avspoof-spoof')
def test_avspoof_spoof():
    database = bob.bio.base.load_resource('physical_access-spoof', 'database', preferred_package='bob.bio.spear')
    try:
        check_database(database, groups=('dev', 'eval'), training_depends=True)
    except IOError as e:
        raise SkipTest(
            "The database could not queried; probably the db.sql3 file is missing. Here is the error: '%s'" % e)

@db_available('asvspoof-spoof')
def test_asvspoof_spoof():
    database = bob.bio.base.load_resource('ASV-female-spoof', 'database', preferred_package='bob.bio.spear')
    try:
        check_database(database, groups=('dev', 'eval'), training_depends=True, skip_train=True)
    except IOError as e:
        raise SkipTest(
            "The database could not queried; probably the db.sql3 file is missing. Here is the error: '%s'" % e)
