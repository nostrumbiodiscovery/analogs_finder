import pytest
import os
import glob
from analogs_finder import main as an

DIR = os.path.dirname(__file__)
RESULT_TRESH=1
RESULT_COMBI_SEARCH=2
RESULT_SIMILAR=4
RESULT_SUBSTRUCTURE=2
RESULT_SUBSTRUCTURE_ATOMS_TO_GROW=1
RESULT_SUBSTRUCTURE_ATOMS_TO_AVOID=2
RESULT_SUBSTRUCTURE_ATOMS_TO_AVOID2=1
RESULT_HYBRID=2
RESULT_ONLYPOSTFILTER=5
RESULT_ONLYPOSTFILTER2=1

MOLECULE = [os.path.join(DIR, "data/substructre_1.sdf"), ]
MOLECULES = glob.glob(os.path.join(DIR, "data/substructre_*.sdf"))
DB = os.path.join(DIR, "data/database.sdf")
SUBSTRUCTURE = os.path.join(DIR, "data/substructre_3.sdf")

def test_tresh(molecule=MOLECULE, db=DB, result=RESULT_TRESH):
    output = an.query_database(db, molecule, treshold=0.45)
    assert result == output


def test_combi(molecule=MOLECULES, db=DB, result=RESULT_COMBI_SEARCH):
    output = an.query_database(db, molecule, combi_subsearch=True)
    assert result == output

def test_similar(molecule=MOLECULE, db=DB, result=RESULT_SIMILAR):
    output = an.query_database(db, molecule, most_similars=True, n_structs=result)
    assert result == output

def test_substructure(molecule=MOLECULE, db=DB, result=RESULT_SUBSTRUCTURE):
    output = an.query_database(db, molecule, substructure=True)
    assert result == output

def test_substructure_atom_to_grow(molecule=MOLECULE, db=DB, result=RESULT_SUBSTRUCTURE_ATOMS_TO_GROW):
    output = an.query_database(db, molecule, substructure=True, atoms_to_grow=[1])
    assert result == output

def test_substructure_atom_to_avoid(molecule=MOLECULE, db=DB, result=RESULT_SUBSTRUCTURE_ATOMS_TO_AVOID):
    output = an.query_database(db, molecule, substructure=True, atoms_to_avoid=[7])
    assert result == output

def test_substructure_atom_to_avoid_2(molecule=MOLECULE, db=DB, result=RESULT_SUBSTRUCTURE_ATOMS_TO_AVOID2):
    output = an.query_database(db, molecule, substructure=True, atoms_to_avoid=[4])
    assert result == output

def test_hybrid(molecule=MOLECULE, db=DB, substructures=SUBSTRUCTURE, treshold=0.1, result=RESULT_HYBRID):
    output = an.query_database(db, molecule, hybrid=substructures, treshold=treshold)
    assert result == output

def test_tresh_all_fps(molecule=MOLECULE, db=DB, result=RESULT_TRESH):
    output = an.query_database(db, molecule, treshold=[0.7, 0.4, 0.4, 0.27], fp_type=["DL", "circular", "torsions", "MACCS"])
    assert result == output

def test_only_postfilter(molecule=MOLECULE, db=DB, result=RESULT_ONLYPOSTFILTER):
    output = an.query_database(db, molecule, treshold=[0.7, 0.4, 0.4, 0.27], fp_type=["DL", "circular", "torsions", "MACCS"], only_postfilter=True)
    assert result == output

def test_only_postfilter(molecule=MOLECULE, db=DB, result=RESULT_ONLYPOSTFILTER2):
    output = an.query_database(db, molecule, treshold=[0.7, 0.4, 0.4, 0.27], fp_type=["DL", "circular", "torsions", "MACCS"], only_postfilter=True, atoms_to_grow=[1])
    assert result == output
