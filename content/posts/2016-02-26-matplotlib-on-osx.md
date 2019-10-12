---
title: Python & Matplotlib on OSX
tags: ['python']
status: published
description: Where we discuss two ways of installing Matplotlib on MacOS.
---


One day, we will hopefully have a grand unified build and package management
system for Python where everything is free & open and Just Works (TM).  Until
then, you have two options:

## brew Python + pip

1. `brew install python3`
2. `pyvenv -v ~/envs/py3`
3. `source ~/envs/py3/bin/activate`
4. `pip install matplotlib`

Pros/cons:

 - Pip is the standard Python package management tool, and uses the official
   Python Package Index (PyPi) repository.
 - Wheels on PyPi are built by authors themselves from open recipes.
 - Binary wheels may not be available for all packages.
 - Pip is not the best of package management tools.

## Conda

1. Download and install miniconda
2. `conda create -n py3 python=3.5 matplotlib`
3. `source activate py3`

Pros/cons:

  - Conda is a great package management tool.
  - Conda environments are well tested; almost everything works out of the
    box.  This includes fast linear algebra using MKL.
  - Some of the conda build recipes are closed and binary wheels may not be
    available for all packages[^1].
  - Conda and pip do not always play well together.
  - Conda packages are supported almost exclusively by a single company.

[^1]: Some members of the community maintain [their own channels](https://conda-forge.github.io), but there are still some issues to
be aware of when [mixing those channels and the official ones](https://github.com/conda-forge/conda-forge.github.io/issues/22).
