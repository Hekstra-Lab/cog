import os

def softlimits(image=None, cell=None, spacegroup=None, distance=None,
               center=None, resolution=2.0, spot_profile=(10, 5, 2.0),
               inpfile="limits.inp", logfile="limits.log",
               outfile="spots.spt"):
    """
    Determine soft limits for data analsysis using Precognition's spot 
    profile and resolution estimates

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
    """
    # Check arguments
    if not os.path.exists(image):
        raise ValueError(f"Image {image} does not exist")
    if not distance:
        raise ValueError("Please provide a detector distance")
    if (not center) or (len(center) != 2):
        raise ValueError("Please provide valid coordinates for the beam center")

    # Write input file
    cellformatted = " ".join([ f"{d:.3f}" for d in cell ])
    inptext = (f"diagnostic    off\n"
               f"busy          off\n"
               f"Input\n"
               f"   Crystal    {cellformatted} {spacegroup}\n"
               f"   Distance   {distance:.3f}\n"
               f"   Center     {center[0]:.3f} {center[1].3f}\n"
               f"   Pixel      0.0886 0.0886\n"
               f"   Omega      0 0\n"
               f"   Goniometer 0 0 0\n"
               f"   Format     RayonixMX340\n"
               f"   Image      {image}\n"
               f"   Resolution {resolution:.2f} 100\n"
               f"   Wavelength 1.02 1.16\n"
               f"   Quit\n"
               f"Spot {spot_profile[0]:d} {spot_profile[1]:d} {spot_profile[2]:.2f} {outfile}\n"
               f"Profile\n"
               f"Limits\n"
               f"Quit\n"
    )
    with open(inpfile, "w") as inp:
        inp.write(inptext)

    return
