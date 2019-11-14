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
    parser_softlimits.add_argument("-i", "--image", help="image to use for determining soft limits")
    parser_softlimits.set_defaults(func=softlimits)
    
    # Parse commandline arguments and call subcommand
    args = vars(parser.parse_args())
    func = args.pop("func")
    func(**args)
    
if __name__ == "__main__":
    main()
