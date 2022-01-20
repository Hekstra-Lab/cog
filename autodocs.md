# **cog** Module Overview

short description

## Classes
* `Experiment`

    ```
    
    Laue crystallography experiment for processing in Precognition.

    Provides a set of attributes and methods that can be used for
    representing and analyzing Laue diffraction experiments.
    
    ```

  * `Experiment.images`

      ```
      DataFrame containing images in Experiment and associated metadata
      ```

  * `Experiment.pathToImages`

      ```
      Path to directory containing image files
      ```

  * `Experiment.distance`

      ```
      Detector distance in mm
      ```

  * `Experiment.center`

      ```
      Beam center in pixels
      ```

  * `Experiment.pixelSize`

      ```
      Pixel size in mm
      ```

  * `Experiment.cell`

      ```
      
        Unit cell parameters for crystal
        
      ```

  * `Experiment.spacegroup`

      ```
      
        Spacegroup number (int)
        
      ```

  * `Experiment.numImages`

      ```
      
        Number of images in Experiment
        
      ```

  * `Experiment.invertGoniometerRotation`

      ```
      
        Invert rotation of goniometer for images in Experiment
        
      ```

  * `Experiment.toPickle`
  * `Experiment.fromPickle`
  * `Experiment.fromDataSet`

      ```
      
        Initialize Experiment from a DataSet object. This function is only
        here to maintain backwards compatibility with old versions of cog.

        Parameters
        ----------
        dataset : cog.core.DataSet
            DataSet object from cog (DEPRECATED)
        
      ```

  * `Experiment.fromLogs`

      ```
      
        Initialize Experiment from a list of log files from BioCARS.

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
        
      ```

  * `Experiment.softlimits`

      ```
      
        Determine the soft limits for data analysis in Precognition.

        Parameters
        ----------
        image : str
            Filename of image to select from Experiment.images DataFrame
        resolution : float
            High-resolution limit in angstroms
        spot_profile : tuple(length, width, sigma-cut)
            Parameters to be used for spot recognition
        
      ```

  * `Experiment.index`

      ```
      
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
        
      ```

  * `Experiment.refine`

      ```
      
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
        
      ```

  * `Experiment.calibrate`

      ```
      
        Calibrate experimental geometry for image using Precognition

        Parameters
        ----------
        image : str
            Filename of image to select from Experiment.images
        resolution : float
            High-resolution limit in angstroms
        spot_profile : tuple(length, width, sigma-cut)
            Parameters to be used for spot recognition
        
      ```

* `FrameGeometry`





