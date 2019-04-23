import pytest
from rdkit import Chem
import os
import glob
from analogs_finder.helpers import helpers as hp

RESULT = 4
DIR = os.path.dirname(__file__)
DB = os.path.join(DIR, "data/database.sdf")

def test_duplicates(db=DB, result=RESULT):
    mols = Chem.SDMolSupplier(db)
    output = hp.remove_duplicates(mols)
    assert len(output) == result

