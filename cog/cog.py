import argparse


def main():

    # Top-level parser
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title="Precognition data reduction stages")

    # Parser for softlimits
    parser_softlimits = subparsers.add_parser("softlimits",
                                              help="Determine soft limits for data analysis")
    parser_softlimits.add_argument("-i", "--image", help="image to use for determining soft limits")

    # Parse commandline arguments
    parser.parse_args()
    
if __name__ == "__main__":
    main()
