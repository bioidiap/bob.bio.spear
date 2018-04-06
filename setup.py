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

from setuptools import setup, dist
dist.Distribution(dict(setup_requires=['bob.extension']))

from bob.extension.utils import load_requirements, find_packages
install_requires = load_requirements()

# The only thing we do in this file is to call the setup() function with all
# parameters that define our package.
setup(

    # This is the basic information about your project. Modify all this
    # information before releasing code publicly.
    name = 'bob.bio.spear',
    version = open("version.txt").read().rstrip(),
    description = 'Tools for running speaker recognition experiments',

    url = 'https://gitlab.idiap.ch/bob/bob.bio.spear',
    license = 'GPLv3',
    author = 'Andre Anjos',
    author_email = 'andre.anjos@idiap.ch',
    keywords = 'bob, biometric recognition, evaluation',

    # If you have a better, long description of your package, place it on the
    # 'doc' directory and then hook it here
    long_description = open('README.rst').read(),

    # This line is required for any distutils based packaging.
    packages = find_packages(),
    include_package_data = True,
    zip_safe=False,

    # This line defines which packages should be installed when you "install"
    # this package. All packages that are mentioned here, but are not installed
    # on the current system will be installed locally and only visible to the
    # scripts of this package. Don't worry - You won't need administrative
    # privileges when using buildout.
    install_requires = install_requires,

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
    entry_points = {

      'bob.bio.database': [
        'timit            = bob.bio.spear.config.database.timit:database',
        'mobio-audio-male       = bob.bio.spear.config.database.mobio_audio_male:database',
        'mobio-audio-female       = bob.bio.spear.config.database.mobio_audio_female:database',
        'avspoof-licit             = bob.bio.spear.config.database.avspoof:database_licit',
        'avspoof-spoof             = bob.bio.spear.config.database.avspoof:database_spoof',
        'asvspoof-licit             = bob.bio.spear.config.database.asvspoof:database_licit',
        'asvspoof-spoof             = bob.bio.spear.config.database.asvspoof:database_spoof',
        'voicepa-licit             = bob.bio.spear.config.database.voicepa:database_licit',
        'voicepa-spoof             = bob.bio.spear.config.database.voicepa:database_spoof',
        'asvspoof2017-licit             = bob.bio.spear.config.database.asvspoof2017:database_licit',
        'asvspoof2017-spoof             = bob.bio.spear.config.database.asvspoof2017:database_spoof',
      ],

      'bob.bio.preprocessor': [
        'cqcc20p            = bob.bio.spear.config.extractor.cqcc20:cqcc20',  # Empty preprocessor for CQCC features
        'energy-2gauss = bob.bio.spear.config.preprocessor.energy_2gauss:preprocessor', # two Gauss energy
        'energy-thr        = bob.bio.spear.config.preprocessor.energy_thr:preprocessor', # thresholded energy
        'mod-4hz           = bob.bio.spear.config.preprocessor.mod_4hz:preprocessor', # mod_4hz
        'external            = bob.bio.spear.config.preprocessor.external:preprocessor', # external VAD
      ],

      'bob.bio.extractor': [
        'cqcc20e = bob.bio.spear.config.extractor.cqcc20:cqcc20',  # Extractor (reads Matlab files) for CQCC features
        'mfcc-60    = bob.bio.spear.config.extractor.mfcc_60:extractor', # 60-dim MFCC features
        'lfcc-60      = bob.bio.spear.config.extractor.lfcc_60:extractor', # 60-dim LFCC features
        'htk            = bob.bio.spear.config.extractor.htk:extractor', # HTK features
        'spro          = bob.bio.spear.config.extractor.spro:extractor', # SPRO features
        # 20 SSFCs with delta and delta-delta
        'ssfc20  = bob.bio.spear.config.extractor.ssfc20:extractor',
        # 20 SCFCs with delta and delta-delta
        'scfc20  = bob.bio.spear.config.extractor.scfc20:extractor',
        # 20 SCMCs with delta and delta-delta
        'scmc20  = bob.bio.spear.config.extractor.scmc20:extractor',
        # 20 RFCCs with delta and delta-delta
        'rfcc20  = bob.bio.spear.config.extractor.rfcc20:extractor',
        # 20 MFCC with delta and delta-delta
        'mfcc20  = bob.bio.spear.config.extractor.mfcc20:extractor',
        # 20 IMFCC with delta and delta-delta
        'imfcc20  = bob.bio.spear.config.extractor.imfcc20:extractor',
        # 20 LFCCs with delta and delta-delta
        'lfcc20  = bob.bio.spear.config.extractor.lfcc20:extractor',
      ],

      'bob.bio.algorithm': [
        'gmm-voxforge      = bob.bio.spear.config.algorithm.gmm_voxforge:algorithm', # GMM config used for voxforge
        'ivec-cosine-voxforge  = bob.bio.spear.config.algorithm.ivec_cosine_voxforge:algorithm', # IVec Cosine config used for voxforge
        'ivec-plda-voxforge     = bob.bio.spear.config.algorithm.ivec_plda_voxforge:algorithm', # IVec PLDA used for voxforge
        'isv-voxforge               = bob.bio.spear.config.algorithm.isv_voxforge:algorithm', # ISV config used for voxforge
        'jfa-voxforge               = bob.bio.spear.config.algorithm.jfa_voxforge:algorithm', # JFA config used for voxforge
        'gmm-timit                  = bob.bio.spear.config.algorithm.gmm_timit:algorithm', # GMM config used for TIMIT
        'gmm-banca                = bob.bio.spear.config.algorithm.gmm_regular_banca:algorithm', # GMM config used for BANCA
        'ivec-plda-mobio         = bob.bio.spear.config.algorithm.ivec_plda_mobio:algorithm', # IVec PLDA used for MOBIO
        'isv-mobio         = bob.bio.spear.config.algorithm.isv_mobio:algorithm', # ISV used for MOBIO
        'ivec-avspoof  = bob.bio.spear.config.algorithm.ivec_avspoof:algorithm',  # IVec PLDA used for AVspoof
        # I-Vector config used for AVspoof
        'isv-avspoof  = bob.bio.spear.config.algorithm.isv_avspoof:algorithm',  # ISV config used for AVspoof
        # GMM training algorithm as per the paper "A Comparison of Features for Synthetic Speech Detection"
        'gmm-tomi  = bob.bio.spear.config.algorithm.gmm_tomi:algorithm',
        # the same as above but with smaller thresholds
        'gmm-tomi-scfc  = bob.bio.spear.config.algorithm.gmm_tomi_scfc:algorithm',
      ],

      'bob.bio.grid':[
        'modest         = bob.bio.spear.config.grid.modest:grid',
      ],
   },

    # Classifiers are important if you plan to distribute this package through
    # PyPI. You can find the complete list of classifiers that are valid and
    # useful here (http://pypi.python.org/pypi?%3Aaction=list_classifiers).
    classifiers = [
      'Framework :: Bob',
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
      'Natural Language :: English',
      'Programming Language :: Python',
      'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
)
