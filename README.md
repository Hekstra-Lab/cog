# cog
[![Build](https://github.com/Hekstra-Lab/cog/actions/workflows/build.yml/badge.svg)](https://github.com/Hekstra-Lab/cog/actions/workflows/build.yml)  

We are not yet `postcog`... but this is at least better than `precog`.

This package is intended to serve as a lightweight Python wrapper for
`Precognition` that facilitates common Laue data reduction routines. `cog`
provides a Python module that can be loaded in other Python scripts or IPython/Jupyter
notebooks, as well as a convenience function, `cog`, that can be called from the
commandline.

I don't foresee this being useful outside of our research group at the moment, so I
am hardcoding a few Odyssey-specific paths/features into this package. For now, that
is the only place we have `Precognition` installed.

## Installation Instructions

```
pip install git+https://github.com/Hekstra-Lab/cog.git
```
Note that because this repo is private (for now, and perhaps forever) you'll be asked to authenticate when you try to run the above. If you haven't already, you might need to [set up a GitHub personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)

## The [`cog.Experiment`](https://github.com/Hekstra-Lab/cog/blob/documentation/autodocs.md#experiment) object
The [`cog.Experiment`](https://github.com/Hekstra-Lab/cog/blob/documentation/autodocs.md#experiment) object is the core of the `cog` data processing pipeline. Get yourself access to this object via:
```python
from cog import Experiment
```
The first thing you'll want to do is create an `Experiment`; the easiest way to do this is via the [`import_from_logs`](https://github.com/Hekstra-Lab/cog/blob/documentation/autodocs.md#import_from_logs) function, which pulls information out of a BioCARS log file. For example:


#### Quick note on this documentation
I (Dennis) fell down a rabbit hole that led me to [this](https://github.com/Hekstra-Lab/cog/blob/documentation/autodocs.md), a cleaned-up version of the relevant docstrings from useful `cog` functions. I made this using [my lightly modified fork](https://github.com/dennisbrookner/doc2md) of [this repo](https://github.com/oiao/doc2md).
