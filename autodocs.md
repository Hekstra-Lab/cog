# `cog`

A wrapper around `precognition`

# Functions
## `import_from_logs`


    Create Experiment object from BioCARS log files and provided metadata.

    Parameters
    ----------
    logs : list of filepaths
        List of log files to initialize Experiment
    distance : float
        Detector distance in mm. If not given, the nominal distance
        will be read from the log files
    center : tuple of floats (len of 2)
        Beam center in pixels
    pixelSize : tuple of floats (len of 2)
        Pixel size along fast- and slow-axis of detector in mm
    cell : tuple of floats (len of 6)
        Cell parameters of crystal
    spacegroup : int
        Space group number
    output : str
        Output file to which Experiment object will be written (.pkl file)
     
## `index`


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
    matrix : list or tuple (len==9)
        Missetting rotation matrix
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
     
## `refine`


    Refine experimental geometry for image using Precognition.

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
     
## `calibrate`


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
     


# Classes
## `Experiment`
Laue crystallography experiment for processing in Precognition.

Provides a set of attributes and methods that can be used for
representing and analyzing Laue diffraction experiments.
### Properties of `Experiment` 
* #### `Experiment.images`
`DataFrame containing images in Experiment and associated metadata` 
* #### `Experiment.pathToImages`
`Path to directory containing image files` 
* #### `Experiment.distance`
`Detector distance in mm` 
* #### `Experiment.center`
`Beam center in pixels` 
* #### `Experiment.pixelSize`
`Pixel size in mm` 
* #### `Experiment.cell`
`Unit cell parameters for crystal` 
* #### `Experiment.spacegroup`
`Spacegroup number (int)` 
* #### `Experiment.numImages`
`Number of images in Experiment` 
### Methods of `Experiment` 
#### `Experiment.invertGoniometerRotation`


        Invert rotation of goniometer for images in Experiment
         
#### `Experiment.toPickle`
#### `Experiment.fromPickle`
#### `Experiment.softlimits`


        Determine the soft limits for data analysis in Precognition.

        Parameters
        ----------
        image : str
            Filename of image to select from Experiment.images DataFrame
        resolution : float
            High-resolution limit in angstroms
        spot_profile : tuple(length, width, sigma-cut)
            Parameters to be used for spot recognition
         
#### `Experiment.index`


        Index image using Precognition

        Parameters
        ----------
        image : str
            Filename of image to select from Experiment.images DataFrame
        reference_geometry : str
            Filename of image to use for missetting matrix
        resolution : float
            High-resolution limit in angstroms
        spot_profile : tuple(length, width, sigma-cut)
            Parameters to be used for spot recognition
         
#### `Experiment.refine`


        Refine experimental geometry for image using Precognition

        Parameters
        ----------
        image : str
            Filename of image to select from Experiment.images
        initial_geometry : str
            Filename of image to use for initial geometry from Experiment.images.
            Defaults to using the same image
        resolution : float
            High-resolution limit in angstroms
        spot_profile : tuple(length, width, sigma-cut)
            Parameters to be used for spot recognition
         
#### `Experiment.calibrate`


        Calibrate experimental geometry for image using Precognition

        Parameters
        ----------
        image : str
            Filename of image to select from Experiment.images
        resolution : float
            High-resolution limit in angstroms
        spot_profile : tuple(length, width, sigma-cut)
            Parameters to be used for spot recognition
         
## `FrameGeometry`




