#!/usr/bin/env python
"""
Load DataSet from logs or .pkl file and embed in IPython shell.
"""

import argparse
from cog import DataSet
from IPython import embed

def main():

    # CLI
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                     description=__doc__)
    parser.add_argument("input", nargs="+", help="Input files to load (.pkl or .log)")
    args = parser.parse_args()

    # Load .pkl
    if len(args.input) == 1 and args.input[0].endswith(".pkl"):
        ds = DataSet.fromPickle(args.input[0])
    
    # Otherwise, load all .log files
    elif all([ i.endswith(".log") for i in args.input ]):
        ds = DataSet.fromLogs(sorted(args.input))

    else:
        raise ValueError("Can only accept one .pkl or one or more .log files")

    # Spin up IPython shell
    bold = '\033[1m'
    end  = '\033[0m'
    header = f"cog.DataSet loaded as {bold}ds{end}"
    embed(colors='neutral', header=header)
        
if __name__ == "__main__":
    main()
