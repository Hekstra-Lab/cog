from os.path import isdir, abspath, dirname, join
import pandas as pd
import pickle


class Experiment:
    """
    Laue crystallography experiment for processing in Precognition.

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
        format="RayonixMX340",
    ):

        # Initialize attributes
        self.images = images
        self.pathToImages = pathToImages
        self.distance = distance
        self.center = center
        self.pixelSize = pixelSize
        self.cell = cell
        self.spacegroup = spacegroup
        self.format = format
        return

    # -------------------------------------------------------------------#
    # Attributes

    @property
    def images(self):
        """DataFrame containing images in Experiment and associated metadata"""
        return self._images

    @images.setter
    def images(self, val):
        if not isinstance(val, pd.DataFrame):
            raise ValueError(f"Experiment.images should be set with a DataFrame")
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
        Number of images in Experiment
        """
        return len(self.images)

    @property
    def format(self):
        """Image format to use by Precognition"""
        return self._format

    @format.setter
    def format(self, val):
        self._format = val


    # ----------------------------------------------------------------------#
    # Methods

    def __repr__(self):
        """String representation of Experiment instance"""
        return f"<cog.Experiment with {self.numImages} frames>"

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
        Invert rotation of goniometer for images in Experiment
        """
        self.images["phi"] *= -1
        return

    def toPickle(self, pklfile="experiment.pkl"):
        with open(pklfile, "wb") as pkl:
            pickle.dump(self, pkl, protocol=pickle.HIGHEST_PROTOCOL)
        return

    @staticmethod
    def fromPickle(pklfile):
        with open(pklfile, "rb") as pkl:
            ds = pickle.load(pkl)
        return ds

    @classmethod
    def fromDataSet(cls, dataset):
        """
        Initialize Experiment from a DataSet object. This function is only
        here to maintain backwards compatibility with old versions of cog.

        Parameters
        ----------
        dataset : cog.core.DataSet
            DataSet object from cog (DEPRECATED)
        """
        from cog.core.dataset import DataSet

        assert isinstance(dataset, DataSet)

        return cls(
            images=dataset.images,
            pathToImages=dataset.pathToImages,
            distance=dataset.distance,
            center=dataset.center,
            pixelSize=dataset.pixelSize,
            cell=dataset.cell,
            spacegroup=dataset.spacegroup,
        )

    @classmethod
    def fromLogs(
        cls,
        logs,
        distance=None,
        center=None,
        pixelSize=(0.08854, 0.08854),
        cell=None,
        spacegroup=None,
        acq_num=None,
    ):
        """
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
        acq_num : str
            The "new FPGA" files are parsed for either "acquisition 5.10.4" or "acquisition 6.2.8".
            If your log file contains "acquisition" + some different number, provide that number here.
            Defaults to None.
        """
        dists = []
        dfs = []
        pathToImages = abspath(dirname(logs[0]))
        oldFPGA = None
        for log in logs:
            with open(log, "r") as f:
                line1 = f.readline()

                # Handle old FPGA
                if "Lauecollect" in line1:
                    oldFPGA = True
                    lines18 = [line1] + [f.readline() for i in range(17)]
                    dists.append(float(lines18[7].split()[3]))
                    dfs.append(pd.read_csv(f, delimiter="\t"))

                # Handle new FPGA
                elif ("acquisition 5.10.4" in line1) or ("acquisition 6.2.8" in line1):
                    oldFPGA = False
                    lines2 = [line1, f.readline()]
                    dfs.append(pd.read_csv(f, delimiter="\t"))

                # Maybe this number will change again in the future? Adding support for that
                elif acq_num is not None:
                    if f"acquisition {acq_num}" in line1:
                        oldFPGA = False
                        lines2 = [line1, f.readline()]
                        dfs.append(pd.read_csv(f, delimiter="\t"))

                # Catch all other log files
                else:
                    raise ValueError(
                        "I don't recognize this log file format -- blame Jack and/or Dennis"
                    )

        # Only old FPGA has the nominal detector distance in the logs
        if oldFPGA:
            if all(d == dists[0] for d in dists):
                dist = dists[0]
            else:
                raise ValueError("At least one log has a different detector distance!")
        else:
            dist = None

        if distance:
            dist = distance

        # Adjust the DataFrame to remove extra columns
        df = pd.concat(dfs)
        if oldFPGA:
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
            df.loc[df["delay"] == "-", "delay"] = "off"
        else:
            df = df[["#date time", "file", "Delay", "HuberPhi"]]
            df.rename(
                columns={"#date time": "time", "Delay": "delay", "HuberPhi": "phi"},
                inplace=True,
            )
            df["delay"] *= 1e9  # convert to ns
            df.loc[df["delay"].isna(), "delay"] = "off"
            df["delay"] = df["delay"].apply(
                lambda x: x if x == "off" else f"{int(x)}ns"
            )

        df.reset_index(inplace=True, drop=True)
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
            Filename of image to select from Experiment.images DataFrame
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
            Filename of image to select from Experiment.images DataFrame
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
            self.format,
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
            Filename of image to select from Experiment.images
        initial_geometry : str
            Filename of image to use for initial geometry from Experiment.images.
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
            Filename of image to select from Experiment.images
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
