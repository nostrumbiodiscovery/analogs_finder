import pytest
import os
import glob
from analogs_finder import main as an



DIR = os.path.dirname(__file__)
RESULT_FP_DL=1

MOLECULE = [os.path.join(DIR, "data/substructre_1.sdf"), ]
DB = os.path.join(DIR, "data/database.sdf")



def test_fp_type(molecule=MOLECULE, db=DB, fp_type="circular", result=RESULT_FP_DL):
    output = an.query_database(db, molecule, treshold=0.45, fp_type=fp_type)
    assert result != output
