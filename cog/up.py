#!/usr/bin/env python
"""
Plot the orientation of the crystal in the lab coordinate frame from a 
Precognition geometry file.

Note: This currently only works correctly for the vertical goniometer used in EF-X
"""

import argparse
from cog import FrameGeometry
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

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
    u = axis
    sin,cos = np.sin(angle),np.cos(angle)
    return cos*np.eye(3) + sin*np.cross(u, -np.eye(3)) + (1. - cos)*np.outer(u, u)

def angle(v1, v2):
    return np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))

def plotUnitCell(a, b, c, ax):
    
    origin = np.array([0, 0, 0])
    
    # Plot a vectors
    ax.quiver(*origin, *a, arrow_length_ratio=0.01, color='r', label=r"$\vec{a}$")
    for vec in [b, c, b+c]:
        ax.quiver(*vec, *a, arrow_length_ratio=0.01, color='r')
        
    # Plot b vectors
    ax.quiver(*origin, *b, arrow_length_ratio=0.01, color='g', label=r"$\vec{b}$")
    for vec in [a, c, a+c]:
        ax.quiver(*vec, *b, arrow_length_ratio=0.01, color='g')
        
    # Plot c vectors
    ax.quiver(*origin, *c, arrow_length_ratio=0.01, color='b', label=r"$\vec{c}$")
    for vec in [a, b, a+b]:
        ax.quiver(*vec, *c, arrow_length_ratio=0.01, color='b')
   
    return

def main():

    # CLI
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                     description=__doc__)
    parser.add_argument("inp", nargs="+",
                        help="Precognition geometry file (suffixed with .mccd.inp)")
    args = parser.parse_args()

    # Plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    plt.title("Lab Coordinate System")

    # Load geometry
    for inp in args.inp:
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
        A = np.rot90(np.linalg.inv((A_star.T)), 3)
        a = A[0, :]
        b = A[1, :]
        c = A[2, :]

        plotUnitCell(a, b, c, ax)

        # Compute angles between EF and each cell axis
        print(inp)
        theta_a = np.rad2deg(angle(a, np.array([0, -1, 0])))
        theta_b = np.rad2deg(angle(b, np.array([0, -1, 0])))
        theta_c = np.rad2deg(angle(c, np.array([0, -1, 0])))
        print(f"Angle between a axis and EF: {theta_a:.3f} deg")
        print(f"Angle between b axis and EF: {theta_b:.3f} deg")
        print(f"Angle between c axis and EF: {theta_c:.3f} deg")        
        print("----------------------------------------------")
        
    maxvec = np.linalg.norm(A, 2, 0).max()
    ax.quiver(*[0, 0, -1.5*maxvec], *[0, 0, 3*maxvec], arrow_length_ratio=0.1, alpha=0.75, color="k", label="X-ray")
    ax.quiver(*[0, 1.5*maxvec, 0], *[0, -3*maxvec, 0], arrow_length_ratio=0.1, alpha=0.75, color="y", label="EF")

    # Adjust axes
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.set_xlim(-2*maxvec, 2*maxvec)
    ax.set_ylim(-2*maxvec, 2*maxvec)
    ax.set_zlim(-2*maxvec, 2*maxvec)
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys(), loc='center left', bbox_to_anchor=(1, 0.5), title="Precog")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
