def softlimits(image=None, cell=None, distance=None, center=None,
               resolution=2.0, spot_profile=(10, 5, 2.0), outfile="spots.spt"):
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
    distance : float
        Detector distance in mm
    center : tuple(center_x, center_y)
        Coordinates of beam center in pixels
    resolution : float
        High-resolution limit in angstroms
    spot_profile : tuple(length, width, sigma-cut)
        Parameters to be used for spot recognition
    outfile : filename
        File to which spot locations should be written
    """
    print(image)
    print(cell)
    print(distance)
    print(center)
    print(resolution)
    print(spot_profile)
    print(outfile)
    return
