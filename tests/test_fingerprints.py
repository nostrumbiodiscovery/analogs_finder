import pytest
import os
import glob
from analogs_finder import main as an



DIR = os.path.dirname(__file__)
RESULT_TRESH=1
RESULT_COMBI_SEARCH=2
RESULT_SIMILAR=4
RESULT_SUBSTRUCTURE=2
RESULT_HYBRID=2

MOLECULE = [os.path.join(DIR, "data/substructre_1.sdf"), ]
MOLECULES = glob.glob(os.path.join(DIR, "data/substructre_*.sdf"))
DB = os.path.join(DIR, "data/database.sdf")



def test_fp_type(molecule=MOLECULE, db=DB, fp_type="circular", result=RESULT_TRESH):
    output = an.query_database(db, molecule, treshold=0.45, fp_type=fp_type, allow_repetition=True)
    assert result != output
