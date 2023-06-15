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
    spack_source = "/n/holylfs05/LABS/hekstra_lab/Lab/garden/lib/spack/share/spack/setup-env.sh"
    garden = "/n/holylfs05/LABS/hekstra_lab/Lab/garden"
    precognition = f"{garden}/precognition/Precognition_5.2_distrib"

    # Commands
    setenv = f"source {spack_source}; spack load gcc; source {precognition}/setup_precog_spack.sh"
    precog = f"Precognition_T5.2.2_x86_64 {inpfile} > {logfile}"
    cmd = f"{setenv}; {precog}"

    # Run command
    subprocess.call(cmd, shell=True)
