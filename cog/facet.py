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

def orthogonalization_matrix(a, b, c, alpha, beta, gamma):
    """
    Compute Cartesian orthogonalization matrix from unit cell parameters
    """
    # Convert unit cell angles to radians
    alpha = np.deg2rad(alpha)
    beta = np.deg2rad(beta)
    gamma = np.deg2rad(gamma)
    
    # Compute unit cell volume
    V = (a*b*c*np.sqrt(1 - np.cos(alpha)**2 -
                       np.cos(beta)**2 -
                       np.cos(gamma)**2 +
                       2*np.cos(alpha)*np.cos(beta)*np.cos(gamma)))
    
    # Compute Cartesian orthogonalization matrix (Rupp, Page 746)
    O = np.zeros((3, 3))
    O[0, 0] = a
    O[0, 1] = b*np.cos(gamma)
    O[1, 1] = b*np.sin(gamma)
    O[0, 2] = c*np.cos(beta)
    O[1, 2] = c*(np.cos(alpha) - (np.cos(beta)*np.cos(gamma)))/np.sin(gamma)
    O[2, 2] = V/(a*b*np.sin(gamma))
    return O

def get_rotation_matrix(axis, angle):
    """Get rotation matrix corresponding to axis-angle convention"""
    u = axis
    sin,cos = np.sin(angle),np.cos(angle)
    return cos*np.eye(3) + sin*np.cross(u, -np.eye(3)) + (1. - cos)*np.outer(u, u)

def angle(v1, v2):
    """Compute angle between two vectors"""
    return np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))

def get_unitcell_vectors(inp):
    """
    Get real-space unit cell vectors in the lab reference frame from a 
    Precognition refined geometry file (*.mccd.inp)
    """
    geometry = FrameGeometry(inp)
    cell = list(map(float, geometry.crystal))
    missetting = np.array(geometry.matrix, dtype=np.float).reshape(3, 3)
    O = orthogonalization_matrix(*cell).T
    
    # Compute goniometer rotation matrix
    o1 = np.deg2rad(float(geometry.omega[0]))
    o2 = np.deg2rad(float(geometry.omega[1]))    
    gonio_phi = np.deg2rad(float(geometry.goniometer[2]))
    R = get_rotation_matrix(np.array([0., 0., -1.]),  o1)
    R = get_rotation_matrix(np.array([0., 1., 0.]), o2)@R
    R = get_rotation_matrix((R@np.array([0., 1., 0.])[:,None])[:,0], gonio_phi)@R
    
    # Compute A-matrix
    precog2mosflm = np.array(
        [[  0,  0,  1],
         [  0, -1,  0],
         [  1,  0,  0]]
    ) 
    A_star = precog2mosflm@(R@missetting@np.linalg.inv(O))
    A = np.linalg.inv(A_star)
    a, b, c = A
    return a, b, c

def main():

    # CLI
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                     description=__doc__)
    parser.add_argument("inp", nargs="+",
                        help="Precognition geometry file (suffixed with .mccd.inp)")
    args = parser.parse_args()

    # Relevant Miller planes
    facets = list(itertools.product([-1, 0, 1], repeat=3))
    facets.remove((0, 0, 0))

    # Initialize results lists
    l_facets = []
    l_images = []
    l_angles = []
    
    # Load geometry
    for inp in args.inp:
        a, b, c = get_unitcell_vectors(inp)
        for facet in facets:
            h, k, l = facet
            normal = h*a + k*b + l*c
            theta = np.rad2deg(angle(normal, np.array([0, -1, 0])))
            l_facets.append(facet)
            l_images.append(inp)
            l_angles.append(theta)

    # Format output
    df = pd.DataFrame({"Facet": l_facets, "Image": l_images, "Angle": l_angles})
    results = df.groupby("Facet").agg({"Angle":["mean", "std", "count"]})
    results.sort_values(("Angle", "mean"), inplace=True)
    print(results)
    
if __name__ == "__main__":
    main()
