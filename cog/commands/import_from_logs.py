from cog.core import Experiment

def import_from_logs(
    logs=None,
    distance=None,
    center=None,
    pixelsize=None,
    cell=None,
    spacegroup=None,
    output=None,
):
    """
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
    """
    if not output.endswith(".pkl"):
        raise ValueError(f"Output suffix must be .pkl -- given: {output}")

    dataset = Experiment.fromLogs(logs, distance, center, pixelsize, cell, spacegroup)
    dataset.toPickle(output)
    return
