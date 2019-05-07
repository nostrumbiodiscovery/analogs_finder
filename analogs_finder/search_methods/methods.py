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

def search_most_similars(molecule_query, molecules_db, n_structs, fp_type="DL"):
    molecules_most_similar = [0] * n_structs
    similarity = np.zeros(n_structs)
    for s, m in tqdm(compute_similarity(molecule_query, molecules_db, fp_type)):
        idx = np.argmin(similarity)
        less_similar = similarity[idx]
        if s > less_similar:
            similarity[idx] = s
            m.SetProp("Similarity", str(s))
            molecules_most_similar[idx] = m
    molecules_most_similar = [ m for m in molecules_most_similar if m != 0 ]
    return molecules_most_similar

def search_similarity_tresh(molecule_query, molecules_db, treshold, fp_type="DL"):
    for s, m in tqdm(compute_similarity(molecule_query, molecules_db, fp_type)):
        if s > treshold:
            m.SetProp("Similarity", str(s))
            yield m

def search_similarity_tresh_several_fp(molecule_query, molecules_db, tresholds=[0.7, 0.4, 0.7, 0.4], fp_types=["DL", "circular", "torsions", "MACCS"]):
    assert len(tresholds) == len(fp_types), "Number of fingerprints must be equal to number of tresholds"
    print("Searching most similars...")
    for s, m, j in compute_similarity_severl_fp(molecule_query, molecules_db, fp_types, tresholds):
        fp_name = fp_types[j]
        m.SetProp("Similarity_{}".format(fp_name), str(s))
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
            yield m

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
            yield m
 
 

def compute_similarity(mref, molecules, fp_type="DL"):
    fp_ref = fps.fingerprint(mref, fp_type)
    for i, m in enumerate(molecules):
        if m:
            fp = fps.fingerprint(m, fp_type)
            yield DataStructs.FingerprintSimilarity(fp_ref, fp), m
        else:
            print("Molecule {}".format(i))

def compute_similarity_severl_fp(mref, molecules, fp_types=["DL", "circular", "torsions", "MACCS"], tresholds=[0.7, 0.4, 0.7, 0.4]):
    for i, m in tqdm(enumerate(molecules)):
        chosen = False
        for j, fp_type in enumerate(fp_types):
            fp_ref = fps.fingerprint(mref, fp_type=fp_type)
            if not chosen:
                fp = fps.fingerprint(m, fp_type=fp_type)
                s = DataStructs.FingerprintSimilarity(fp_ref, fp)
                if m:
                    if s > float(tresholds[j]):
                        chosen = True
                        yield s, m, j
                else:
                    print("Molecule {}".format(i))
            else:
                break

def most_similar_with_substructure(molecule_query, molecules_db, substructures, treshold, fp_type="DL"):
    for s, m in tqdm(compute_similarity(molecule_query, molecules_db, fp_type)):
        # Similarity based
        if s > treshold:
            for substruct in Chem.SDMolSupplier(substructures):
                # Substructure based
                if m.HasSubstructMatch(substruct, useChirality=True):
                    m.SetProp("Similarity", str(s))
                    yield m

    
