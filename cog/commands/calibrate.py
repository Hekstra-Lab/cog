import os
from cog import FrameGeometry
from cog.core.precognition import run


def calibrate(
    image,
    phi,
    geometry,
    pathToImages,
    format="RayonixMX340",
    resolution=2.0,
    spot_profile=(6, 4, 4),
    inpfile="calibrate.inp",
    logfile="calibrate.log",
):
    """
    Calibrate experimental geometry for image using Precognition.

    Parameters
    ----------
    image : filename
        Path to image to be analyzed. For now, it is assumed to be a
        MCCD image from a RayonixMX340 detector
    phi : float
        Phi angle of goniometer
    geometry : cog.FrameGeometry
        Experimental geometry from which to initialize refinement
    pathToImages : str
        Path to directory containing the MCCD images
    format  : string (optional)
        Image format to use by Precognition 
    resolution : float
        High-resolution limit in angstroms
    spot_profile : tuple(length, width, sigma-cut)
        Parameters to be used for spot recognition
    inpfile : filename
        File to which Precognition input will be written
    logfile : filename
        File to which Precognition log will be written

    Returns
    -------
    (rmsd, numMatched, geometry) : (float, int, cog.FrameGeometry)
        RMSD in pixels between recognized and predicted spots
        Number of matched spots
        Refined experimental geometry for image
    """
    # Check arguments
    if not os.path.exists(os.path.join(pathToImages, image)):
        raise ValueError(f"Image {image} does not exist")
    if not isinstance(geometry, FrameGeometry):
        raise ValueError(f"{geometry} is not of type {type(FrameGeometry)}")

    # Write geometry file
    geometry.writeINPFile(f"{image}.inp")

    # Write input file
    inptext = (
        f"diagnostic    off\n"
        f"busy          off\n\n"
        f"@{image}.inp\n\n"
        f"Input\n"
        f"   Crystal    0.05 0.05 0.05 0.05 0.05 0.05 free\n"
        f"   Distance   0.05 free\n"
        f"   Format     {format}\n"
        f"   Resolution {resolution} 100\n"
        f"   Wavelength 1.02 1.18\n"
        f"   Spot       {spot_profile[0]} {spot_profile[1]} {spot_profile[2]}\n"
        f"   Quit\n"
        f"Dataset       calibration\n"
        f"   In	      {pathToImages}\n"
        f"   Quit\n"
        f"Quit\n"
    )
    with open(inpfile, "w") as inp:
        inp.write(inptext)

    run(inpfile, logfile)
    return checkStatus(image, logfile)


def checkStatus(image, logfile):
    """
    Return status of geometry refinement. RMSDs and matched spots are
    determined by grepping for RMSD  lines in the logfile:

    Example line:
    R.M.S.D. in pixel & matched spots:     0.52 508

    Parameters
    ----------
    image : str
        Name of image used for geometry refinement
    logfile : str
        Filename of logfile from Precognition refinement

    Returns
    -------
    (rmsd, numMatched, geometry) : (float, int, cog.FrameGeometry)
        RMSD in pixels between recognized and predicted spots
        Number of matched spots
        Refined experimental geometry for image
    """
    # Check for error statement in logfile
    with open(logfile, "r") as log:
        lines = log.readlines()

    rmsdlines = [l for l in lines if "R.M.S.D" in l]
    if len(rmsdlines) > 1:
        raise NotImplementedError(
            (f"Jack hasn't implemented parsing " f"multiple RMSD entries yet...")
        )
    else:
        fields = rmsdlines[0].split()
        rmsd = float(fields[6])
        numMatched = int(fields[7])

    return rmsd, numMatched, FrameGeometry(f"{image}.inp")
