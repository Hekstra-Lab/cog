from os.path import isdir, abspath, dirname
import pandas as pd
import pickle

class DataSet():
    """
    Laue crystallography dataset for processing in Precognition.

    Provides a set of attributes and methods that can be used for 
    representing and analyzing Laue diffraction experiments.
    """

    def __init__(self, images, pathToImages, distance=None, center=None,
                 pixelSize=(0.0886, 0.0886), cell=None, sg=None):

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
        if not isinstance(center, tuple):
            raise ValueError("Beam center must be a tuple of floats")
        else:
            self.center = center

        # Pixel size in (mm, mm)
        if not isinstance(pixelSize, tuple):
            raise ValueError("Pixel size must be a tuple of floats")
        else:
            self.pixelSize = pixelSize

        # Cell parameters for crystal
        if not isinstance(cell, tuple) or len(cell) != 6:
            raise ValueError("Cell must be specified as (a, b, c, alpha, beta, gamma)")
        else:
            setCell(self, *cell)

        # Space group for crystal
        self.sg = sg
            
        return
            
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
    
    def numImages(self):
        """
        Number of images in DataSet

        Returns
        -------
        int : Number of images
        """
        return len(data.images)
        
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
    def fromLogs(cls, logs, distance=None, center=None):
        """
        Initialize DataSet from a list of log files from BioCARS.

        Parameters
        ----------
        logs : list of filepaths
            List of log files to initialize DataSet
        distance : float
            Detector distance in mm. If not given, the nominal distance
            will be read from the log files
        center : tuple of floats
            Beam center in pixels
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
        df = df[["#date time", "file", "delay", "Gon Single AX"]]
        df.rename(columns={"#date time": "time", "Gon Single AX": "phi"},
                  inplace=True)
        df.reset_index(inplace=True, drop=True)
        df.loc[df["delay"] == "-", "delay"] = "off"

        return cls(images=df, pathToImages=pathToImages, distance=dist,
                   center=center)
            
