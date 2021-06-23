import os
from cog import FrameGeometry
from cog.core.precognition import run


def index(
    image,
    cell=None,
    spacegroup=None,
    distance=None,
    center=None,
    phi=0.0,
    resolution=2.0,
    spot_profile=(6, 4, 4),
    inpfile="index.inp",
    logfile="index.log",
    outfile="spots.spt",
):
    """
    Index image using Precognition to determine orientation of crystal
    during diffraction experiment.

    Parameters
    ----------
    image : filename
        Path to image to be analyzed. For now, it is assumed to be a
        MCCD image from a RayonixMX340 detector
    cell : tuple(a, b, c, alpha, beta, gamma)
        Tuple of cell parameters for crystal
    spacegroup : int
        Space group number
    distance : float
        Detector distance in mm
    center : tuple(center_x, center_y)
        Coordinates of beam center in pixels
    phi : float
        Phi angle of goniometer
    resolution : float
        High-resolution limit in angstroms
    spot_profile : tuple(length, width, sigma-cut)
        Parameters to be used for spot recognition
    inpfile : filename
        File to which Precognition input will be written
    logfile : filename
        File to which Precognition log will be written
    outfile : filename
        File to which spot locations will be written

    Returns
    -------
    geometry : cog.FrameGeometry
        Indexed experimental geometry for image (None if failed)
    """
    # Check arguments
    if not os.path.exists(image):
        raise ValueError(f"Image {image} does not exist")
    if not distance:
        raise ValueError("Please provide a detector distance")
    if (not center) or (len(center) != 2):
        raise ValueError("Please provide valid coordinates for the beam center")

    # Write input file
    cellformatted = " ".join([f"{d:.3f}" for d in cell])
    inptext = (
        f"diagnostic    off\n"
        f"busy          off\n"
        f"Input\n"
        f"   Crystal    {cellformatted} {spacegroup}\n"
        f"   Distance   {distance:.3f}\n"
        f"   Center     {center[0]:.3f} {center[1]:.3f}\n"
        f"   Pixel      0.08854 0.08854\n"
        f"   Omega      0 0\n"
        f"   Goniometer 0 0 {phi}\n"
        f"   Format     RayonixMX340\n"
        f"   Image      {image}\n"
        f"   Resolution {resolution:.2f} 100\n"
        f"   Wavelength 1.02 1.16\n"
        f"   Spot       {int(spot_profile[0])} {int(spot_profile[1])}\n"
        f"   Quit\n"
        f"Spot          {spot_profile[2]:.2f} {outfile}\n"
        f"Ellipse       ellipses.spt\n"
        f"Pattern       0 pre.spt\n"
        f"Quit\n"
    )
    with open(inpfile, "w") as inp:
        inp.write(inptext)

    run(inpfile, logfile)
    return checkStatus(logfile)


def checkStatus(logfile):
    """
    Return whether indexing has succeeded or failed.

    Parameters
    ----------
    logfile : str
        Filename of logfile from Precognition indexing

    Returns
    -------
    geometry : cog.FrameGeometry
        Indexed experimental geometry for image (None if failed)
    """
    # Check if indexed geometry has been written
    if not os.path.exists(f"pre.spt.inp"):
        return None

    # Check for error statement in logfile
    with open(logfile, "r") as log:
        lines = log.readlines()
    if [True for l in lines if "Index: Auto-indexing failed!" in l]:
        return None

    return FrameGeometry("pre.spt.inp")
