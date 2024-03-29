#!/usr/bin/env python
"""
Determine the angles between the crystal facets and the electric field 
vector.
"""

import argparse
import itertools
import pandas as pd
import numpy as np
from cog import FrameGeometry


def angle(v1, v2):
    """Compute angle between two vectors"""
    return np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))


def get_normal_vector(hkl, Astar):
    """
    Get normal vector to real-space Miller plane, hkl.

    Note
    ----
        The normal vector to a real-space Miller plane is collinear with
        the reciprocal dHKL vector. As such, we can use this simpler
        formula in the reciprocal lattice basis to get the correct
        orientation in real-space. For a graphical explanation of this,
        please look at Rupp, p238.
    """
    return hkl @ Astar.T


def main():

    # CLI
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter, description=__doc__
    )
    parser.add_argument(
        "inp", nargs="+", help="Precognition geometry file (suffixed with .mccd.inp)"
    )
    parser.add_argument(
        "--hmax",
        default=1,
        help="Maximal number to include in a Miller plane",
        type=int,
    )
    args = parser.parse_args()

    # Relevant Miller planes
    facets = list(itertools.product(np.arange(-args.hmax, args.hmax + 1), repeat=3))
    facets.remove((0, 0, 0))

    # Initialize results lists
    l_facets = []
    l_images = []
    l_angles = []

    # Load geometry
    for inp in args.inp:
        geometry = FrameGeometry(inp)
        Astar = geometry.get_reciprocal_Amatrix()
        for facet in facets:
            hkl = np.array(facet)
            normal = get_normal_vector(hkl, Astar)
            theta = np.rad2deg(angle(normal, np.array([0, -1, 0])))
            l_facets.append(facet)
            l_images.append(inp)
            l_angles.append(theta)

    # Format output
    df = pd.DataFrame({"Facet": l_facets, "Image": l_images, "Angle": l_angles})
    results = df.groupby("Facet").agg({"Angle": ["mean", "std", "count"]})
    results.sort_values(("Angle", "mean"), inplace=True)
    print(results)


if __name__ == "__main__":
    main()
