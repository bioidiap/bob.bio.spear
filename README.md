[![badge doc](https://img.shields.io/badge/docs-latest-orange.svg)](https://www.idiap.ch/software/bob/docs/bob/bob.bio.spear/master/sphinx/index.html)
[![badge pipeline](https://gitlab.idiap.ch/bob/bob.bio.spear/badges/master/pipeline.svg)](https://gitlab.idiap.ch/bob/bob.bio.spear/commits/master)
[![badge coverage](https://gitlab.idiap.ch/bob/bob.bio.spear/badges/master/coverage.svg)](https://www.idiap.ch/software/bob/docs/bob/bob.bio.spear/master/coverage/index.html)
[![badge gitlab](https://img.shields.io/badge/gitlab-project-0000c0.svg)](https://gitlab.idiap.ch/bob/bob.bio.spear)

# Run speaker recognition algorithms

This package is part of the signal-processing and machine learning toolbox
[Bob](https://www.idiap.ch/software/bob).
This package is part of the `bob.bio` packages, which allow to run comparable
and reproducible biometric recognition experiments on publicly available
databases.

This package contains functionality to run speaker recognition experiments.
It is an extension to the
[bob.bio.base](https://pypi.python.org/pypi/bob.bio.base) package, which
provides the basic scripts.
This package contains utilities that are specific for speaker recognition, such
as:

* Audio databases
* Voice activity detection preprocessing
* Acoustic feature extractors
* Recognition algorithms based on acoustic features

For further information about `bob.bio`, please read
[its Documentation](https://www.idiap.ch/software/bob/docs/bob/bob.bio.base/master/sphinx/index.html).

## Installation

Complete Bob's
[installation instructions](https://www.idiap.ch/software/bob/install). Then,
to install this package, run:

``` sh
pip install bob.bio.spear
```

## Contact

For questions or reporting issues to this software package, contact our
development [mailing list](https://www.idiap.ch/software/bob/discuss).
