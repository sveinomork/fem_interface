from pathlib import Path
import pytest
from fem_interface.fem.fem import FEM
@pytest.fixture
def file_path(tmp_path:Path)->Path:
    # Create a temporary file within the pytest temporary directory
    file = tmp_path / "test_file.txt"
    
    # Write the content to the file
    file.write_text("""IDENT     1.00000000E+00  1.10000000E+01  3.00000000E+00  0.00000000E+00
GCOORD    1.00000000E+00  2.64358211E+00  2.71415424E+00  9.47641827E-15
GCOORD    2.00000000E+00  2.60643291E+00  2.73964596E+00 -5.00000007E-02
GCOORD    3.00000000E+00  2.61109447E+00  2.69590259E+00 -5.00000007E-02
GCOORD    4.00000000E+00  2.59928536E+00  2.70923233E+00  5.87419281E-03
GCOORD    5.00000000E+00  2.62500763E+00  2.72690010E+00 -2.50000004E-02
GCOORD    6.00000000E+00  2.60876369E+00  2.71777415E+00 -5.00000007E-02
GCOORD    7.00000000E+00  2.62733841E+00  2.70502830E+00 -2.50000004E-02""")

    return file


def test_read_gcoord(file_path):
    fem_obj=FEM()
    fem_obj.read_fem(file_path)

    
    
  
    assert fem_obj.gcoord[int(float(7.00000000E+00))].xcoord == float(2.62733841E+00 )

    assert fem_obj.gcoord[int(float(1.00000000E+00))].ycoord == float(2.71415424E+00  )

    assert fem_obj.gcoord[int(float(2.00000000E+00))].zcoord == float(-5.00000007E-02  )


