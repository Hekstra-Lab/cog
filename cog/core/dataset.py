from os.path import isdir, abspath, dirname, join
import pandas as pd
import pickle


class DataSet:
    """
    Laue crystallography dataset for processing in Precognition.

    Provides a set of attributes and methods that can be used for
    representing and analyzing Laue diffraction experiments.
    """

    # -------------------------------------------------------------------#
    # Constructor

    def __init__(
        self,
        images,
        pathToImages,
        distance=None,
        center=None,
        pixelSize=(0.08854, 0.08854),
        cell=None,
        spacegroup=None,
    ):

        # Initialize attributes
        self.images = images
        self.pathToImages = pathToImages
        self.distance = distance
        self.center = center
        self.pixelSize = pixelSize
        self.cell = cell
        self.spacegroup = spacegroup

        return

    # -------------------------------------------------------------------#
    # Attributes

    @property
    def images(self):
        """DataFrame containing images in DataSet and associated metadata"""
        return self._images

    @images.setter
    def images(self, val):
        if not isinstance(val, pd.DataFrame):
            raise ValueError(f"DataSet.images should be set with a DataFrame")
        self._images = val

    @property
    def pathToImages(self):
        """Path to directory containing image files"""
        return self._pathToImages

    @pathToImages.setter
    def pathToImages(self, val):
        if not isdir(val):
            raise ValueError(f"Path to images does not exist: {val}")
        self._pathToImages = val

    @property
    def distance(self):
        """Detector distance in mm"""
        return self._distance

    @distance.setter
    def distance(self, val):
        if val is None:
            self._distance = None
        else:
            self._distance = float(val)

    @property
    def center(self):
        """Beam center in pixels"""
        return self._center

    @center.setter
    def center(self, val):
        if val is None:
            self._center = None
        elif not isinstance(val, (tuple, list)):
            raise ValueError("Beam center must be a tuple or list of floats")
        elif len(val) != 2:
            raise ValueError("Beam center must have len()==2")
        else:
            self._center = (float(val[0]), float(val[1]))

    @property
    def pixelSize(self):
        """Pixel size in mm"""
        return self._pixelSize

    @pixelSize.setter
    def pixelSize(self, val):
        if val is None:
            self._pixelSize = None
        elif not isinstance(val, (tuple, list)):
            raise ValueError("Pixel size must be a tuple or list of floats")
        elif len(val) != 2:
            raise ValueError("Pixel size must have len()==2")
        else:
            self._pixelSize = (float(val[0]), float(val[1]))

    @property
    def cell(self):
        """
        Unit cell parameters for crystal
        """
        return (self.a, self.b, self.c, self.alpha, self.beta, self.gamma)

    @cell.setter
    def cell(self, values):
        if values is None:
            self._setCell(*[None] * 6)
        elif not isinstance(values, (tuple, list)):
            raise ValueError("cell must be a tuple or list of floats")
        elif len(values) != 6:
            raise ValueError("Cell must be specified as (a, b, c, alpha, beta, gamma)")
        else:
            self._setCell(*values)

    @property
    def spacegroup(self):
        """
        Spacegroup number (int)
        """
        return self._spacegroup

    @spacegroup.setter
    def spacegroup(self, val):
        if val is None:
            self._spacegroup = None
        else:
            self._spacegroup = int(val)

    @property
    def numImages(self):
        """
        Number of images in DataSet
        """
        return len(self.images)

    # ----------------------------------------------------------------------#
    # Methods

    def __repr__(self):
        """String representation of DataSet instance"""
        return f"<cog.DataSet with {self.numImages} frames>"

    def _setCell(self, a, b, c, alpha, beta, gamma):
        self.a = a
        self.b = b
        self.c = c
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        return

    def invertGoniometerRotation(self):
        """
        Invert rotation of goniometer for images in DataSet
        """
        self.images["phi"] *= -1
        return

    def toPickle(self, pklfile="DataSet.pkl"):
        with open(pklfile, "wb") as pkl:
            pickle.dump(self, pkl, protocol=pickle.HIGHEST_PROTOCOL)
        return

    @staticmethod
    def fromPickle(pklfile):
        with open(pklfile, "rb") as pkl:
            ds = pickle.load(pkl)
        return ds

    @classmethod
    def fromLogs(
        cls,
        logs,
        distance=None,
        center=None,
        pixelSize=(0.08854, 0.08854),
        cell=None,
        spacegroup=None,
    ):
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
        spacegroup : int
            Space group number
        """
        dists = []
        dfs = []
        pathToImages = abspath(dirname(logs[0]))
        for log in logs:
            with open(log, "r") as f:
                lines18 = [f.readline() for i in range(18)]
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
        if "Gon Single AX" in df.columns:
            df = df[["#date time", "file", "delay", "Gon Single AX"]]
        elif "angle" in df.columns:
            df = df[["#date time", "file", "delay", "angle"]]
        else:
            raise ValueError(
                "Could not determine gonio angle field in log -- blame Jack"
            )
        df.rename(
            columns={"#date time": "time", "Gon Single AX": "phi", "angle": "phi"},
            inplace=True,
        )

        df.reset_index(inplace=True, drop=True)
        df.loc[df["delay"] == "-", "delay"] = "off"
        df.set_index("file", inplace=True)

        return cls(
            images=df,
            pathToImages=pathToImages,
            distance=dist,
            center=center,
            pixelSize=pixelSize,
            cell=cell,
            spacegroup=spacegroup,
        )

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

        softlimits(
            imagepath,
            self.cell,
            self.spacegroup,
            self.distance,
            self.center,
            resolution,
            spot_profile,
        )

        return

    def index(
        self, image, reference_geometry=None, resolution=2.0, spot_profile=(6, 4, 4.0)
    ):
        """
        Index image using Precognition

        Parameters
        ----------
        image : str
            Filename of image to select from DataSet.images DataFrame
        reference_geometry : str
            Filename of image to use for missetting matrix
        resolution : float
            High-resolution limit in angstroms
        spot_profile : tuple(length, width, sigma-cut)
            Parameters to be used for spot recognition
        """
        from cog.commands import index

        try:
            entry = self.images.loc[image]
            phi = entry["phi"]
            imagepath = join(self.pathToImages, image)
            if reference_geometry:
                matrix = self.images.loc[reference_geometry, "geometry"].matrix
            else:
                matrix = None
        except KeyError:
            raise KeyError(f"{image} was not found in image DataFrame")

        geom = index(
            imagepath,
            self.cell,
            self.spacegroup,
            self.distance,
            self.center,
            phi,
            resolution,
            spot_profile,
            matrix=matrix,
        )

        if geom:
            self.images.loc[image, "geometry"] = geom

        return

    def refine(
        self, image, initial_geometry=None, resolution=2.0, spot_profile=(6, 4, 4.0)
    ):
        """
        Refine experimental geometry for image using Precognition

        Parameters
        ----------
        image : str
            Filename of image to select from DataSet.images
        initial_geometry : str
            Filename of image to use for initial geometry from DataSet.images.
            Defaults to using the same image
        resolution : float
            High-resolution limit in angstroms
        spot_profile : tuple(length, width, sigma-cut)
            Parameters to be used for spot recognition
        """
        from cog.commands import refine

        try:
            entry = self.images.loc[image]
            phi = entry["phi"]
            if initial_geometry is None:
                geometry = entry["geometry"]
            else:
                geometry = self.images.loc[initial_geometry, "geometry"]
        except KeyError:
            raise KeyError(f"{image} was not found in image DataFrame")

        rmsd, numMatched, geom = refine(
            image, phi, geometry, self.pathToImages, resolution, spot_profile
        )
        self.images.loc[image, "geometry"] = geom
        self.images.loc[image, "rmsd"] = rmsd
        self.images.loc[image, "matched"] = numMatched

        return rmsd

    def calibrate(self, image, resolution=2.0, spot_profile=(6, 4, 4.0)):
        """
        Calibrate experimental geometry for image using Precognition

        Parameters
        ----------
        image : str
            Filename of image to select from DataSet.images
        resolution : float
            High-resolution limit in angstroms
        spot_profile : tuple(length, width, sigma-cut)
            Parameters to be used for spot recognition
        """
        from cog.commands import calibrate

        try:
            entry = self.images.loc[image]
            phi = entry["phi"]
            geometry = entry["geometry"]
        except KeyError:
            raise KeyError(f"{image} was not found in image DataFrame")

        rmsd, numMatched, geom = calibrate(
            image, phi, geometry, self.pathToImages, resolution, spot_profile
        )
        self.images.loc[image, "geometry"] = geom
        self.images.loc[image, "rmsd"] = rmsd
        self.images.loc[image, "matched"] = numMatched

        return
