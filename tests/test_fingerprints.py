import pytest
import os
import glob
from analogs_finder import main as an



DIR = os.path.dirname(__file__)
RESULT_FP_DL=1

MOLECULE = [os.path.join(DIR, "data/substructre_1.sdf"), ]
DB = os.path.join(DIR, "data/database.sdf")
MOLECULE_CIRCULAR = [os.path.join(DIR, "data/query_circular.sdf"),]
DB_CIRCULAR = os.path.join(DIR, "data/db_circular.sdf")


def test_fp_type(molecule=MOLECULE, db=DB, fp_type="circular", result=RESULT_FP_DL):
    output = an.query_database(db, molecule, treshold=0.45, fp_type=fp_type)
    assert result != output

def test_circular(molecule=MOLECULE_CIRCULAR, db=DB_CIRCULAR, fp_type="circular", result=18):
    output = an.query_database(db, molecule, treshold=0.4, fp_type=fp_type)
    assert result == output

def test_pharm(molecule=MOLECULE_CIRCULAR, db=DB_CIRCULAR, fp_type="pharm", result=12):
    output = an.query_database(db, molecule, treshold=0.4, fp_type=fp_type)
    assert result == output

