import pytest
import pandas as pd

from cog import DataSet

def test_constructor_minimal():
    """Test minimal DataSet constructor"""
    ds = DataSet(pd.DataFrame(), "./")

    assert ds.distance is None
    assert ds.center is None
    assert isinstance(ds.pixelSize, tuple)
    assert ds.pixelSize == (0.08854, 0.08854)
    assert ds.cell == (None, None, None, None, None, None)
    assert ds.spacegroup is None


@pytest.mark.parametrize("images", [pd.DataFrame()])
@pytest.mark.parametrize("pathToImages", ["./"])
@pytest.mark.parametrize("distance", [None, 100, 100.0])
@pytest.mark.parametrize("center", [
    None,
    (1990, 1970),
    [1990,  1970],
    (1991., 1970.),
    [1990., 1970.]
])
@pytest.mark.parametrize("pixelSize", [
    None,
    (88, 88),
    [88,  88],
    (88.6, 88.6),
    [88.6, 88.6]
])
@pytest.mark.parametrize("cell", [
    None,
    [1., 2., 3., 90., 90., 90.],
    (1., 2., 3., 90., 90., 90.)
])
@pytest.mark.parametrize("spacegroup", [
    None,
    1,
    19,
    96,
    1.0
])
def test_constructor(images, pathToImages, distance, center, pixelSize, cell, spacegroup):
    """Test DataSet constructor"""
    ds = DataSet(images,
                 pathToImages,
                 distance=distance,
                 center=center,
                 pixelSize=pixelSize,
                 cell=cell,
                 spacegroup=spacegroup)

    if distance is None:
        assert ds.distance is None
    else:
        assert ds.distance == float(distance)

    if center is None:
        assert ds.center is None
    else:
        assert isinstance(ds.center, tuple)
        assert ds.center == (float(center[0]), float(center[1]))

    if pixelSize is None:
        assert ds.pixelSize is None
    else:
        assert isinstance(ds.pixelSize, tuple)
        assert ds.pixelSize == (float(pixelSize[0]), float(pixelSize[1]))

    if cell is None:
        assert ds.cell == tuple([None]*6)
    else:
        assert ds.cell == (cell[0], cell[1], cell[2], cell[3], cell[4], cell[5])

    if spacegroup is None:
        assert ds.spacegroup is None
    else:
        assert ds.spacegroup == int(spacegroup)

