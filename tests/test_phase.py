import pytest
import time
import os
from analogs_finder.rank_methods import phase as ps

DIR = os.path.dirname(__file__)
MOLECULE = os.path.join(DIR, "data/substructre_1.sdf")
DB = os.path.join(DIR, "data/database.sdf")
HYPO = os.path.join(DIR, "data/substructre_1.phypo")
RESULT = "query_molec_phase-hits.maegz"
TIME = 30

def test_phase(molecule=MOLECULE, db=DB):
    if os.path.exists(RESULT):
        os.remove(RESULT)
    ps.run_phase_screen(molecule, db)
    time.sleep(60)
    assert os.path.exists(RESULT)
    

def test_phase_external_hypo(molecule=MOLECULE, db=DB, hypotesis=HYPO):
    if os.path.exists(RESULT):
        os.remove(RESULT)
    ps.run_phase_screen(molecule, db, hypotesis=HYPO)
    time.sleep(TIME)
    assert os.path.exists(RESULT)

def test_phase_no_minimization(molecule=MOLECULE, db=DB, hypotesis=HYPO):
    if os.path.exists(RESULT):
        os.remove(RESULT)
    ps.run_phase_screen(molecule, db, hypotesis=HYPO, minimization=False)
    time.sleep(TIME)
    assert os.path.exists(RESULT)

def test_phase_match(molecule=MOLECULE, db=DB, hypotesis=HYPO):
    if os.path.exists(RESULT):
        os.remove(RESULT)
    ps.run_phase_screen(molecule, db, hypotesis=HYPO, match=4)
    time.sleep(TIME)
    assert os.path.exists(RESULT)
