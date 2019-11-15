# cog
We are not yet `postcog`... but this is at least better than `precog`.

This package is intended to serve as a lightweight Python wrapper for
`Precognition` that facilitates common Laue data reduction routines. `cog`
provides a Python module that can be loaded in other Python scripts or IPython/Jupyter
notebooks, as well as a convenience function, `cog`, that can be called from the
commandline.

I don't foresee this being useful outside of our research group at the moment, so I
am hardcoding a few Odyssey-specific paths/features into this package. For now, that
is the only place we have `Precognition` installed.
