# cog
[![Build](https://github.com/Hekstra-Lab/cog/actions/workflows/build.yml/badge.svg)](https://github.com/Hekstra-Lab/cog/actions/workflows/build.yml)  

We are not yet `postcog`... but this is at least better than `precog`.

This package is intended to serve as a lightweight Python wrapper for
`Precognition` that facilitates common Laue data reduction routines. `cog`
provides a Python module that can be loaded in other Python scripts or IPython/Jupyter
notebooks, as well as a convenience function, `cog`, that can be called from the
commandline.

## Installation Instructions

This is a pure python library that can be installed as:

```shell
pip install git+https://github.com/Hekstra-Lab/cog.git
```

Note that this repo is private, so you'll need to enter your github credentials (unless they're already cached, which is fairly likely).

### Development install
If you'll be actively developing the `cog` source code, you should clone the repo and install in "editable" (`-e`) mode:
```shell
git clone https://github.com/Hekstra-Lab/cog.git
cd cog
pip install -e .
```

## Note about hard-coding
The `cog` library is intended to be used for processing BioCARS Laue data using
precognition, so I see it most useful as a private repo for use in our group. This
way we can avoid providing "general" support/features, and can tailor things more
to our specific usage and context. Specifically, there are Odyssey paths/features
hardcoded in to make things easy to use on the Harvard cluster. 

This package can be installed locally so that you can read `Experiment` .pkl files
for plotting, analysis, etc. However, you won't be able to run precognition data
processing locally.
