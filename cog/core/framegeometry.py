import os

class FrameGeometry():
    """
    Provides a representation of  per-frame geometry in Precognition.

    Includes attributes for accessing geometric parameters, and methods
    for reading and writing Precognition .inp geometry files. 
    """

    def __init__(self, inpfile):
        self.readINPFile(inpfile)

    @property
    def crystal(self):
        return self.__crystal

    @crystal.setter
    def crystal(self, values):
        if len(values) != 6:
            raise ValueError(f"Cell parameters must have 6 values")
        values = *map(float, values),
        self.__crystal = values
        return

    @property
    def spacegroup(self):
        return self.__spacegroup

    @spacegroup.setter 
    def spacegroup(self, value):
        self.__spacegroup = value
        return

    @property
    def matrix(self):
        return self.__matrix

    @matrix.setter
    def matrix(self, values):
        self.__matrix = values
        return

    @property
    def omega(self):
        return self.__omega

    @spacegroup.setter
    def omega(self, values):
        self.__omega = values
        return

    @property
    def goniometer(self):
        return self.__goniometer

    @goniometer.setter
    def goniometer(self, values):
        self.__goniometer = values
        return

    @property
    def imageformat(self):
        return self.__imageformat

    @imageformat.setter
    def imageformat(self, value):
        self.__imageformat = value
        return

    @property
    def distance(self):
        return self.__distance

    @distance.setter
    def distance(self, values):
        self.__distance = values
        return

    @property
    def center(self):
        return self.__center

    @center.setter
    def center(self, values):
        self.__center = values
        return

    @property
    def pixel(self):
        return self.__pixel

    @pixel.setter
    def pixel(self, values):
        self.__pixel = values
        return

    @property
    def swing(self):
        return self.__swing

    @swing.setter
    def swing(self, values):
        self.__swing = values
        return

    @property
    def tilt(self):
        return self.__tilt

    @tilt.setter
    def tilt(self, values):
        self.__tilt = values
        return
    
    @property
    def bulge(self):
        return self.__bulge

    @bulge.setter
    def bulge(self, values):
        self.__bulge = values
        return

    @property
    def image(self):
        return self.__image

    @image.setter
    def image(self, value):
        self.__image = value
        return

    @property
    def resolution(self):
        return self.__resolution

    @resolution.setter
    def resolution(self, values):
        self.__resolution = values
        return

    @property
    def wavelength(self):
        return self.__wavelength

    @wavelength.setter
    def wavelength(self, values):
        self.__wavelength = values
        return
    
    def readINPFile(self, inpfile):
        """
        Read Precognition .inp file and update geometric attributes

        Parameters
        ----------
        inpfile : str
            Path to .inp file from which to read

        Notes
        -----
        It is assumed that the format of the .inp file is as follows:

        Input
           Field1     Values1
           Field2     Values2
           ...
           Quit
        """
        # Check that inpfile exists
        if not os.path.exists(inpfile):
            raise ValueError(f"Cannot find file: {inpfile}")

        # Read inpfile
        with open(inpfile, "r") as inp:
            lines = inp.readlines()
        if not ("Input" in lines[0] and "Quit" in lines[-1]):
            raise ValueError(f"{inpfile} does not meet formatting assumptions")

        # Parse geometric parameters
        geometry = {}
        for l in lines[1:-1]:
            fields = l.split()
            if fields != []:
                geometry[fields[0]] = fields[1:]

        for key, values in geometry.items():
            if key == "Crystal":
                self.crystal = values[:-1]
                self.spacegroup = values[-1]
            elif key == "Matrix":
                self.matrix = values
            elif key == "Omega":
                self.omega = values
            elif key == "Goniometer":
                self.goniometer = values
            elif key == "Format":
                self.imageformat = values
            elif key == "Distance":
                self.distance = values
            elif key == "Center":
                self.center = values
            elif key == "Pixel":
                self.pixel = values
            elif key == "Swing":
                self.swing = values
            elif key == "Tilt":
                self.tilt = values
            elif key == "Bulge":
                self.bulge = values
            elif key == "Image":
                self.image = values
            elif key == "Resolution":
                self.resolution = values
            elif key == "Wavelength":
                self.wavelength = values
            else:
                raise ValueError(f"Unexpected key {key} in {inpfile}")
                
        return
                
    def writeINPFile(self, inpfile):
        """
        Write Precognition .inp file containing experimental geometry

        Parameters
        ----------
        inpfile : str
            Path to .inp file to which to write
        """
        
