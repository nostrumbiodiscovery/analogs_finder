import pytest
from rdkit import Chem
import os
import glob
from analogs_finder.helpers import helpers as hp
from analogs_finder.search_methods import molecule as ml

RESULT = 4
DIR = os.path.dirname(__file__)
DB = os.path.join(DIR, "data/database.sdf")

def test_duplicates(db=DB, result=RESULT):
    mols = Chem.SDMolSupplier(db)
    mols = [ml.Molecule(m) for m in mols]
    output = hp.remove_duplicates(mols)
    assert len(output) == result

