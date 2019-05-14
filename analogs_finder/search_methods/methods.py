import argparse
import sys
from functools import partial
import collections
from tqdm import tqdm
import numpy as np
from rdkit import Chem
from rdkit import DataStructs
from multiprocessing import Pool
from analogs_finder.search_methods import fingerprints as fps
from analogs_finder.search_methods import similarity as sm
from analogs_finder.search_methods import molecule as ml

def search_most_similars(molecule_query, molecules_db, n_structs, fp_type="DL"):
    molecules_most_similar = [0] * n_structs
    similarity = np.zeros(n_structs)
    for m in tqdm(sm.compute_similarity(molecule_query, molecules_db, fp_type)):
        idx = np.argmin(similarity)
        less_similar = similarity[idx]
        if m.similarity > less_similar:
            similarity[idx] = m.similarity
            m.molecule.SetProp("Similarity", str(m.similarity))
            molecules_most_similar[idx] = m
    molecules_most_similar = [ m for m in molecules_most_similar if m != 0 ]
    return molecules_most_similar

def search_similarity_tresh(molecule_query, molecules_db, treshold, fp_type="DL"):
    for m in tqdm(sm.compute_similarity(molecule_query, molecules_db, fp_type)):
        if m.similarity > float(treshold):
            m.molecule.SetProp("Similarity", str(m.similarity))
            yield m

def search_similarity_tresh_several_fp(molecule_query, molecules_db, tresholds=[0.7, 0.4, 0.7, 0.4], fp_types=["DL", "circular", "torsions", "MACCS"]):
    assert len(tresholds) == len(fp_types), "Number of fingerprints must be equal to number of tresholds"
    print("Searching most similars several fingerprint types...")
    for m in sm.compute_similarity_severl_fp(molecule_query, molecules_db, fp_types, tresholds):
        m.molecule.SetProp("Similarity_{}".format(m.fp_type), str(m.similarity))
        yield m

def search_substructure(molecule_query, molecules_db):
    print("Searching for substructure")
    all_substructs_found = True
    for i, m in tqdm(enumerate(molecules_db)):
        if not m:
            print("Skipping {}".format(i))
            continue
        all_substructs_found = True
        for m_ref in molecule_query:
            if not m.HasSubstructMatch(m_ref, useChirality=True):
                all_substructs_found = False
        if all_substructs_found:
            yield ml.molec_properties(m)

def combi_substructure_search(sdfs, molecules_db):
    print("Searching for substructure")
    for i, m in tqdm(enumerate(molecules_db)):
        if not m:
            print("Skipping {}".format(i))
            continue
        substructs_found = [False] * len(sdfs)
        for i, sdf in enumerate(sdfs):
            for m_ref in Chem.SDMolSupplier(sdf):
                if m.HasSubstructMatch(m_ref, useChirality=True):
                    substructs_found[i] = True
        if all(substructs_found):
            yield ml.molec_properties(m)
 

def most_similar_with_substructure(molecule_query, molecules_db, substructures, treshold, fp_type="DL"):
    for m in tqdm(sm.compute_similarity(molecule_query, molecules_db, fp_type)):
        # Similarity based
        if m.similarity > float(treshold):
            for substruct in Chem.SDMolSupplier(substructures):
                # Substructure based
                if m.molecule.HasSubstructMatch(substruct, useChirality=True):
                    m.molecule.SetProp("Similarity", str(m.similarity))
                    yield m

    
