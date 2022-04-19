#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Andre Anjos <andre.anjos@idiap.ch>
# Mon 16 Apr 08:18:08 2012 CEST
#
# Copyright (C) Idiap Research Institute, Martigny, Switzerland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

# This file contains the python (distutils/setuptools) instructions so your
# package can be installed on **any** host system. It defines some basic
# information like the package name for instance, or its homepage.
#
# It also defines which other packages this python package depends on and that
# are required for this package's operation. The python subsystem will make
# sure all dependent packages are installed or will install them for you upon
# the installation of this package.
#
# The 'buildout' system we use here will go further and wrap this package in
# such a way to create an isolated python working environment. Buildout will
# make sure that dependencies which are not yet installed do get installed, but
# **without** requiring administrative privileges on the host system. This
# allows you to test your package with new python dependencies w/o requiring
# administrative interventions.

from setuptools import dist, setup

from bob.extension.utils import find_packages, load_requirements

dist.Distribution(dict(setup_requires=["bob.extension"]))

install_requires = load_requirements()

# The only thing we do in this file is to call the setup() function with all
# parameters that define our package.
setup(
    # This is the basic information about your project. Modify all this
    # information before releasing code publicly.
    name="bob.bio.spear",
    version=open("version.txt").read().rstrip(),
    description="Tools for running speaker recognition experiments",
    url="https://gitlab.idiap.ch/bob/bob.bio.spear",
    license="GPLv3",
    author="Andre Anjos",
    author_email="andre.anjos@idiap.ch",
    keywords="bob, biometric recognition, evaluation",
    # If you have a better, long description of your package, place it on the
    # 'doc' directory and then hook it here
    long_description=open("README.rst").read(),
    # This line is required for any distutils based packaging.
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    # This line defines which packages should be installed when you "install"
    # this package. All packages that are mentioned here, but are not installed
    # on the current system will be installed locally and only visible to the
    # scripts of this package. Don't worry - You won't need administrative
    # privileges when using buildout.
    install_requires=install_requires,
    # Your project should be called something like 'bob.<foo>' or
    # 'bob.<foo>.<bar>'. To implement this correctly and still get all your
    # packages to be imported w/o problems, you need to implement namespaces
    # on the various levels of the package and declare them here. See more
    # about this here:
    # http://peak.telecommunity.com/DevCenter/setuptools#namespace-packages
    #
    # Our database packages are good examples of namespace implementations
    # using several layers. You can check them out here:
    # https://www.idiap.ch/software/bob/packages
    # This entry defines which scripts you will have inside the 'bin' directory
    # once you install the package (or run 'bin/buildout'). The order of each
    # entry under 'console_scripts' is like this:
    #   script-name-at-bin-directory = module.at.your.library:function
    #
    # The module.at.your.library is the python file within your library, using
    # the python syntax for directories (i.e., a '.' instead of '/' or '\').
    # This syntax also omits the '.py' extension of the filename. So, a file
    # installed under 'example/foo.py' that contains a function which
    # implements the 'main()' function of particular script you want to have
    # should be referred as 'example.foo:main'.
    #
    # In this simple example we will create a single program that will print
    # the version of bob.
    entry_points={
        "bob.bio.database": [
            "timit              = bob.bio.spear.config.database.timit:database",
            "mobio-audio-male   = bob.bio.spear.config.database.mobio_audio_male:database",
            "mobio-audio-female = bob.bio.spear.config.database.mobio_audio_female:database",
            "avspoof-licit      = bob.bio.spear.config.database.avspoof:database_licit",
            "avspoof-spoof      = bob.bio.spear.config.database.avspoof:database_spoof",
            "asvspoof-licit     = bob.bio.spear.config.database.asvspoof:database_licit",
            "asvspoof-spoof     = bob.bio.spear.config.database.asvspoof:database_spoof",
            "voicepa-licit      = bob.bio.spear.config.database.voicepa:database_licit",
            "voicepa-spoof      = bob.bio.spear.config.database.voicepa:database_spoof",
            "asvspoof2017-licit = bob.bio.spear.config.database.asvspoof2017:database_licit",
            "asvspoof2017-spoof = bob.bio.spear.config.database.asvspoof2017:database_spoof",
            "voxforge           = bob.bio.spear.config.database.voxforge:database",
            "mini-voxforge      = bob.bio.spear.config.database.mini_voxforge:database",  # For tests only
            "nist-sre04to16     = bob.bio.spear.config.database.nist_sre04to16:database",
        ],
        "bob.bio.annotator": [
            "energy-2gauss = bob.bio.spear.config.annotator.energy_2gauss:annotator",  # Two Gaussian GMM energy VAD
            "energy-thr    = bob.bio.spear.config.annotator.energy_thr:annotator",  # Energy threshold VAD
            "mod-4hz       = bob.bio.spear.config.annotator.mod_4hz:annotator",  # mod_4hz VAD
            "external      = bob.bio.spear.config.annotator.external:annotator",  # external VAD
        ],
        "bob.bio.pipeline": [
            "gmm-voxforge  = bob.bio.spear.config.pipeline.mfcc60_gmm_voxforge:pipeline",
            "isv-voxforge  = bob.bio.spear.config.pipeline.mfcc60_isv_voxforge:pipeline",
            "speechbrain-ecapa-voxceleb   = bob.bio.spear.config.pipeline.speechbrain_ecapa_voxceleb:pipeline",  # Do not call it `speechbrain` as it would try to load the speechbrain module instead
        ],
        "bob.bio.config": [
            # databases:
            "voxforge      = bob.bio.spear.config.database.voxforge",
            "mini-voxforge = bob.bio.spear.config.database.mini_voxforge",
            # PipelineSimple config (pipeline and db):
            "gmm-voxforge  = bob.bio.spear.config.pipeline.mfcc60_gmm_voxforge",
            "gmm-mobio     = bob.bio.spear.config.pipeline.mfcc60_gmm_mobio",
            "isv-voxforge  = bob.bio.spear.config.pipeline.mfcc60_isv_voxforge",
        ],
        "bob.db.cli": [
            "download-voxforge = bob.bio.spear.database.voxforge:download_voxforge",
        ],
    },
    # Classifiers are important if you plan to distribute this package through
    # PyPI. You can find the complete list of classifiers that are valid and
    # useful here (http://pypi.python.org/pypi?%3Aaction=list_classifiers).
    classifiers=[
        "Framework :: Bob",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
