import argparse
import sys
from functools import partial
import collections
from tqdm import tqdm
import numpy as np
from rdkit import Chem
from rdkit import DataStructs
from rdkit.Chem.Fingerprints import FingerprintMols
from multiprocessing import Pool

def search_most_similars(molecule_query, molecules_db, n_structs):
    molecules_most_similar = [0] * n_structs
    similarity = np.zeros(n_structs)
    for s, m in tqdm(compute_similarity(molecule_query, molecules_db)):
        idx = np.argmin(similarity)
        less_similar = similarity[idx]
        if s > less_similar:
            similarity[idx] = s
            m.SetProp("Similarity", str(s))
            molecules_most_similar[idx] = m
    return molecules_most_similar

def search_similarity_tresh(molecule_query, molecules_db, treshold):
    for s, m in tqdm(compute_similarity(molecule_query, molecules_db)):
        if s > treshold:
            m.SetProp("Similarity", str(s))
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
 
 

def compute_similarity(mref, molecules):
    fp_ref = FingerprintMols.FingerprintMol(mref)
    for i, m in enumerate(molecules):
        if m:
            fp = FingerprintMols.FingerprintMol(m)
            yield DataStructs.FingerprintSimilarity(fp_ref, fp), m
        else:
            print("Molecule {}".format(i))

def most_similar_with_substructure(molecule_query, molecules_db, substructures, treshold):
    for s, m in tqdm(compute_similarity(molecule_query, molecules_db)):
        # Similarity based
        if s > treshold:
            for substruct in Chem.SDMolSupplier(substructures):
                # Substructure based
                if m.HasSubstructMatch(substruct, useChirality=True):
                    m.SetProp("Similarity", str(s))
                    yield m

    
