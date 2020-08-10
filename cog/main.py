import argparse
from cog.commands import import_from_logs, softlimits, index


def main():

    # Top-level parser
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title="Precognition data reduction stages",
                                       dest="cmd",
                                       required=True)

    # Parser for import
    parser_import = subparsers.add_parser("import",
                                          help="Create DataSet object from BioCARS log files")
    parser_import.add_argument("logs", nargs="+", help="Log files to import")
    parser_import.add_argument("-d", "--distance", type=float,
                               help=("Detector distance in mm. If not given, nominal distance will"
                                     " be read from the log files"))
    parser_import.add_argument("--center", type=float, nargs=2, metavar=("center_x", "center_y"),
                               help="Coordinates of beam center in pixels")
    parser_import.add_argument("--pixelsize", type=float, nargs=2, default=(0.08854, 0.08854),
                               help="Pixel size of detector in mm")
    parser_import.add_argument("-c", "--cell", help="Cell parameters for crystal",
                               metavar=("a", "b", "c", "alpha", "beta", "gamma"),
                               nargs=6, type=float)
    parser_import.add_argument("--spacegroup", help="Space group number", type=int)
    parser_import.add_argument("-o", "--output", help="Output file (.pkl)",
                               default="dataset.pkl")
    parser_import.set_defaults(cmd=import_from_logs)
    
    # Parser for softlimits
    parser_softlimits = subparsers.add_parser("softlimits",
                                              help="Determine soft limits for data analysis")
    parser_softlimits.add_argument("-i", "--image", help="Image to use for determining soft limits")
    parser_softlimits.add_argument("-c", "--cell", help="Cell parameters for crystal",
                                   metavar=("a", "b", "c", "alpha", "beta", "gamma"),
                                   nargs=6, type=float)
    parser_softlimits.add_argument("--spacegroup", help="Space group number", type=int)
    parser_softlimits.add_argument("-d", "--distance", help="Detector distance in mm",
                                   type=float)
    parser_softlimits.add_argument("--center", help="Coordinates of beam center in pixels",
                                   metavar=("center_x", "center_y"),
                                   nargs=2, type=float)
    parser_softlimits.add_argument("-r", "--resolution", help="High-resolution limit in angstroms",
                                   type=float, default=2.0)
    parser_softlimits.add_argument("-s", "--spot_profile", help="Parameters to be used for spot recognition",
                                   metavar=("length", "width", "sigma_cut"),
                                   nargs=3, type=float, default=[10, 5, 2.0])
    parser_softlimits.add_argument("--inpfile", help="File to which Precognition input will be written",
                                   default="limits.inp")
    parser_softlimits.add_argument("-l", "--logfile", help="File to which Precognition log will be written",
                                   default="limits.log")    
    parser_softlimits.add_argument("-o", "--outfile", help="File to which spot locations will be written",
                                   default="spots.spt")
    parser_softlimits.set_defaults(cmd=softlimits)

    # Parser for index
    parser_index = subparsers.add_parser("index",
                                              help="Index Laue image")
    parser_index.add_argument("-i", "--image", help="Image to use for indexing")
    parser_index.add_argument("-c", "--cell", help="Cell parameters for crystal",
                                   metavar=("a", "b", "c", "alpha", "beta", "gamma"),
                                   nargs=6, type=float)
    parser_index.add_argument("--spacegroup", help="Space group number", type=int)
    parser_index.add_argument("-d", "--distance", help="Detector distance in mm",
                                   type=float)
    parser_index.add_argument("--center", help="Coordinates of beam center in pixels",
                                   metavar=("center_x", "center_y"),
                                   nargs=2, type=float)
    parser_index.add_argument("-p", "--phi", help="Phi angle of goniometer",
                              type=float, default=0.0)
    parser_index.add_argument("-r", "--resolution", help="High-resolution limit in angstroms",
                                   type=float, default=2.0)
    parser_index.add_argument("-s", "--spot_profile", help="Parameters to be used for spot recognition",
                                   metavar=("length", "width", "sigma_cut"),
                                   nargs=3, type=float, default=[10, 5, 2.0])
    parser_index.add_argument("--inpfile", help="File to which Precognition input will be written",
                                   default="limits.inp")
    parser_index.add_argument("-l", "--logfile", help="File to which Precognition log will be written",
                                   default="limits.log")    
    parser_index.add_argument("-o", "--outfile", help="File to which spot locations will be written",
                                   default="spots.spt")
    parser_index.set_defaults(cmd=index)
    
    # Parse commandline arguments and call subcommand
    args = vars(parser.parse_args())
    cmd = args.pop("cmd")
    cmd(**args)
    
if __name__ == "__main__":
    main()
