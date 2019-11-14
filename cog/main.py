import argparse
from cog import softlimits

def main():

    # Top-level parser
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title="Precognition data reduction stages",
                                       dest="cmd",
                                       required=True)

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
                                   type=float)
    parser_softlimits.add_argument("-s", "--spot_profile", help="Parameters to be used for spot recognition",
                                   metavar=("length", "width", "sigma_cut"),
                                   nargs=3, type=float)
    parser_softlimits.add_argument("--inpfile", help="File to which Precognition input will be written")
    parser_softlimits.add_argument("-l", "--logfile", help="File to which Precognition log will be written")    
    parser_softlimits.add_argument("-o", "--outfile", help="File to which spot locations will be written")
    parser_softlimits.set_defaults(cmd=softlimits)
    
    # Parse commandline arguments and call subcommand
    args = vars(parser.parse_args())
    cmd = args.pop("cmd")
    cmd(**args)
    
if __name__ == "__main__":
    main()
