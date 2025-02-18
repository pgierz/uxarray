import os
import xarray as xr

from unittest import TestCase
from pathlib import Path

import uxarray as ux

try:
    import constants
except ImportError:
    from . import constants

current_path = Path(os.path.dirname(os.path.realpath(__file__)))


class TestUgrid(TestCase):

    def test_read_ugrid(self):
        """Reads a ugrid file."""

        ug_filename1 = current_path / "meshfiles" / "outCSne30.ug"
        ug_filename2 = current_path / "meshfiles" / "outRLL1deg.ug"
        ug_filename3 = current_path / "meshfiles" / "ov_RLL10deg_CSne4.ug"

        ux_grid1 = ux.open_dataset(str(ug_filename1))
        ux_grid2 = ux.open_dataset(str(ug_filename2))
        ux_grid3 = ux.open_dataset(str(ug_filename3))

        assert (ux_grid1.Mesh2_node_x.size == constants.NNODES_outCSne30)
        assert (ux_grid2.Mesh2_node_x.size == constants.NNODES_outRLL1deg)
        assert (
            ux_grid3.Mesh2_node_x.size == constants.NNODES_ov_RLL10deg_CSne4)

    def test_read_ugrid_opendap(self):
        """Read an ugrid model from an OPeNDAP URL."""

        url = "http://www.smast.umassd.edu:8080/thredds/dodsC/FVCOM/NECOFS/Forecasts/NECOFS_GOM3_FORECAST.nc"
        ugrid = ux.open_dataset(url, drop_variables="siglay")
        assert isinstance(getattr(ugrid, "Mesh2_node_x"), xr.DataArray)
        assert isinstance(getattr(ugrid, "Mesh2_node_y"), xr.DataArray)
        assert isinstance(getattr(ugrid, "Mesh2_face_nodes"), xr.DataArray)

    def test_write_ugrid(self):
        """Read an exodus file and writes a ugrid file."""

        exo2_filename = current_path / "meshfiles" / "outCSne8.g"
        ux_grid = ux.open_dataset(str(exo2_filename))
        outfile = current_path / "write_test_outCSne8.ug"
        ux_grid.write(str(outfile), "ugrid")
