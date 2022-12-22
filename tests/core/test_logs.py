import pytest
import pandas as pd

from cog import Experiment


@pytest.mark.parametrize("acq_version", ["628", "5104"])
def test_import_log(acq_version):
    """
    Test importing log files with all acceptable versions of "acquisition X.X.X" in line 1
    """
    Experiment.fromLogs([f"tests/data/acq{acq_version}.log"])


def test_import_log_custom():
    """
    Test that a log file with an unexpected acquisition X.X.X header can be imported via
    the acq_num parameter but throws an error otherwise
    """

    path_700 = "tests/data/acq700.log"

    with pytest.raises(ValueError):
        Experiment.fromLogs([path_700])

    Experiment.fromLogs([path_700], acq_num="7.0.0")
