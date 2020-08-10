from os.path import isdir, abspath, dirname, join
import pandas as pd
import pickle

class DataSet():
    """
    Laue crystallography dataset for processing in Precognition.

    Provides a set of attributes and methods that can be used for 
    representing and analyzing Laue diffraction experiments.
    """

    def __init__(self, images, pathToImages, distance=None, center=None,
                 pixelSize=(0.08854, 0.08854), cell=None, sg=None):

        # Set of images stored as a pd.DataFrame
        self.images = images

        # Path to images
        if isdir(pathToImages):
            self.pathToImages = pathToImages
        else:
            raise ValueError(f"Path to images does not exist: {pathToImages}")

        # Detector distance
        self.distance = distance

        # Beam center (pixelX, pixelY)
        if center and not isinstance(center, tuple):
            raise ValueError("Beam center must be a tuple of floats")
        else:
            self.center = center

        # Pixel size in (mm, mm)
        if pixelSize and not isinstance(pixelSize, tuple):
            raise ValueError("Pixel size must be a tuple of floats")
        else:
            self.pixelSize = pixelSize

        # Cell parameters for crystal
        if cell and (not isinstance(cell, tuple) or len(cell) != 6):
            raise ValueError("Cell must be specified as (a, b, c, alpha, beta, gamma)")
        elif cell:
            self.setCell(*cell)
        else:
            self.setCell(*[None]*6)

        # Space group for crystal
        self.sg = sg
            
        return
            
    def __repr__(self):
        """String representation of DataSet instance"""
        return f"<cog.DataSet with {self.numImages} frames>"

    def setCell(self, a, b, c, alpha, beta, gamma):
        self.a = a
        self.b = b
        self.c = c
        self.alpha = alpha
        self.beta  = beta
        self.gamma = gamma
        return

    def getCell(self):
        return (self.a, self.b, self.c, self.alpha, self.beta, self.gamma)

    @property
    def numImages(self):
        """
        Number of images in DataSet

        Returns
        -------
        int : Number of images
        """
        return len(self.images)

    def invertGoniometerRotation(self):
        """
        Invert rotation of goniometer for images in DataSet
        """
        self.images['phi'] *= -1
        return
    
    def toPickle(self, pklfile="DataSet.pkl"):
        with open(pklfile, 'wb') as pkl:
            pickle.dump(self, pkl, protocol=pickle.HIGHEST_PROTOCOL)
        return

    @staticmethod
    def fromPickle(pklfile):
        with open(pklfile, "rb") as pkl:
            ds = pickle.load(pkl)
        return ds

    @classmethod
    def fromLogs(cls, logs, distance=None, center=None, pixelSize=(0.08854, 0.08854),
                 cell=None, sg=None):
        """
        Initialize DataSet from a list of log files from BioCARS.

        Parameters
        ----------
        logs : list of filepaths
            List of log files to initialize DataSet
        distance : float
            Detector distance in mm. If not given, the nominal distance
            will be read from the log files
        center : tuple of floats (len of 2)
            Beam center in pixels
        pixelSize : tuple of floats (len of 2)
            Pixel size along fast- and slow-axis of detector in mm
        cell : tuple of floats (len of 6)
            Cell parameters of crystal
        sg : int
            Space group number
        """
        dists = []
        dfs   = []
        pathToImages = abspath(dirname(logs[0]))
        for log in logs:
            with open(log, "r") as f:
                lines18 = [ f.readline() for i in range(18) ]
                dists.append(float(lines18[7].split()[3]))
                dfs.append(pd.read_csv(f, delimiter="\t"))

        if all(d == dists[0] for d in dists):
            dist = dists[0]
        else:
            raise ValueError("At least one log has a different detector distance!")

        if distance:
            dist = distance
        
        # Adjust the DataFrame to remove extra columns
        df = pd.concat(dfs)
        if "Gon Single Ax" in df.columns:
            df = df[["#date time", "file", "delay", "Gon Single AX"]]
        elif "angle" in df.columns:
            df = df[["#date time", "file", "delay", "angle"]]
        else:
            raise ValueError("Could not determine gonio angle field in log -- blame Jack")
        df.rename(columns={"#date time": "time",
                           "Gon Single AX": "phi",
                           "angle": "phi"},
                  inplace=True)
        
        df.reset_index(inplace=True, drop=True)
        df.loc[df["delay"] == "-", "delay"] = "off"
        df.set_index("file", inplace=True)
        
        return cls(images=df, pathToImages=pathToImages, distance=dist,
                   center=center, pixelSize=pixelSize, cell=cell, sg=sg)
            
    def softlimits(self, image, resolution=2.0, spot_profile=(10, 5, 2.0)):
        """
        Determine the soft limits for data analysis in Precognition. 

        Parameters
        ----------
        image : str
            Filename of image to select from DataSet.images DataFrame
        resolution : float
            High-resolution limit in angstroms
        spot_profile : tuple(length, width, sigma-cut)
            Parameters to be used for spot recognition
        """
        from cog.commands import softlimits

        try:
            _ = self.images.loc[image]
            imagepath = join(self.pathToImages, image)
        except KeyError:
            raise KeyError(f"{image} was not found in image DataFrame")
        
        softlimits(imagepath, self.getCell(), self.sg, self.distance,
                   self.center, resolution, spot_profile)

        return

    def index(self, image, resolution=2.0, spot_profile=(6, 4, 4.0)):
        """
        Index image using Precognition

        Parameters
        ----------
        image : str
            Filename of image to select from DataSet.images DataFrame
        resolution : float
            High-resolution limit in angstroms
        spot_profile : tuple(length, width, sigma-cut)
            Parameters to be used for spot recognition
        """
        from cog.commands import index

        try:
            entry = self.images.loc[image]
            phi = entry['phi']
            imagepath = join(self.pathToImages, image)
        except KeyError:
            raise KeyError(f"{image} was not found in image DataFrame")
        
        geom = index(imagepath, self.getCell(), self.sg, self.distance,
                     self.center, phi, resolution, spot_profile)

        if geom:
            self.images.loc[image, "geometry"] = geom

        return

    def refine(self, image, resolution=2.0, spot_profile=(6, 4, 4.)):
        """
        Refine experimental geometry for image using Precognition

        Parameters
        ----------
        image : str
            Filename of image to select from DataSet.images
        resolution : float
            High-resolution limit in angstroms
        spot_profile : tuple(length, width, sigma-cut)
            Parameters to be used for spot recognition
        """
        from cog.commands import refine

        try:
            entry = self.images.loc[image]
            phi = entry['phi']
            geometry =  entry['geometry']
        except KeyError:
            raise KeyError(f"{image} was not found in image DataFrame")

        rmsd, numMatched, geom = refine(image, phi, geometry,
                                        self.pathToImages, resolution,
                                        spot_profile)
        self.images.loc[image,  "geometry"] = geom
        self.images.loc[image, "rmsd"] = rmsd
        self.images.loc[image, "matched"] = numMatched

        return
