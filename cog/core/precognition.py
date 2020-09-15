import subprocess

def run(inpfile, logfile):
    """
    Run Precognition using the given .inp file and writing all output to
    the designated logfile. 

    Parameters
    ----------
    inpfile : filename
        Input file with Precognition commands
    logfile : filename
        File to which Precognition log will be written
    """
    # Paths
    garden = "/n/holylfs/LABS/hekstra_lab/garden/"
    precognition = f"{garden}/precognition/Precognition_5.2_distrib"

    # Commands
    setenv = f"source {precognition}/setup_precognition_env.sh"
    mktmp  = f"license=$(mktemp /tmp/precoglicense.XXXXXX)"
    cplic  = f"cp $RRILICENSE $license"
    setlic = f"export RRILICENSE=$license"
    precog = f"Precognition_T5.2.2_x86_64 {inpfile} > {logfile}"
    cmd = f"{setenv}; {mktmp}; {cplic}; {setlic}; {precog}"

    # Run command
    subprocess.call(cmd, shell=True)
