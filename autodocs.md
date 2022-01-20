# **cog** Module Overview

A wrapper around `precognition`

## Classes
### `Experiment`
    
    
    Laue crystallography experiment for processing in Precognition.

    Provides a set of attributes and methods that can be used for
    representing and analyzing Laue diffraction experiments.
        
###Properties of Experiment 
#### `Experiment.images`
      ```
      DataFrame containing images in Experiment and associated metadata
      ```
#### `Experiment.pathToImages`
      ```
      Path to directory containing image files
      ```
#### `Experiment.distance`
      ```
      Detector distance in mm
      ```
#### `Experiment.center`
      ```
      Beam center in pixels
      ```
#### `Experiment.pixelSize`
      ```
      Pixel size in mm
      ```
#### `Experiment.cell`
      ```
      
        Unit cell parameters for crystal
        
      ```
#### `Experiment.spacegroup`
      ```
      
        Spacegroup number (int)
        
      ```
#### `Experiment.numImages`
      ```
      
        Number of images in Experiment
        
      ```
###Methods of Experiment 
#### `Experiment.invertGoniometerRotation`

      ```
      
        Invert rotation of goniometer for images in Experiment
        
      ```

#### `Experiment.toPickle`
#### `Experiment.fromPickle`
#### `Experiment.softlimits`

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

#### `Experiment.index`

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

#### `Experiment.refine`

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

#### `Experiment.calibrate`

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






