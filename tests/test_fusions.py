import pytest
import os
import glob
from analogs_finder import main as an



DIR = os.path.dirname(__file__)
MOLECULE = [os.path.join(DIR, "data/substructre_1.sdf"), ]
DB = os.path.join(DIR, "data/database.sdf")




def test_fusion(molecule=MOLECULE, db=DB, fp_type="circular", result=2):
    output = an.query_database(db, molecule, treshold=0.45, fp_type=fp_type, turbo=True, neighbours=1)
    assert result == output
