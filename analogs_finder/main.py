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
from analogs_finder.search_methods import methods as mt



def query_database(database, molecules, n_structs=500, combi_subsearch=False, most_similars=False, substructure=False, output="similars.sdf", treshold=0.7):

    assert type(database) == str, "database must be a unique sdf file"
    assert type(molecules) == list, "query molecule must be a list of a single or multiple sdf files"

    # Database
    molecules_db= Chem.SDMolSupplier(database)

    # Query Molecule
    if most_similars:
        molecule_query = Chem.SDMolSupplier(molecules[0]).next()
    elif combi_subsearch:
        molecule_query = molecules
    elif substructure:
        molecule_query = Chem.SDMolSupplier(molecules[0])
    elif treshold:
        molecule_query = Chem.SDMolSupplier(molecules[0]).next()

    # Method to use
    mol_most_similars = None
    if most_similars:
        mol_most_similars  = mt.search_most_similars(molecule_query, molecules_db, n_structs)
    elif substructure:
        mol_most_similars  = mt.search_substructure(molecule_query, molecules_db)
    elif combi_subsearch:
        mol_most_similars = mt.combi_substructure_search(molecule_query, molecules_db) 
    elif treshold:
        mol_most_similars  = mt.search_similarity_tresh(molecule_query, molecules_db, treshold)
        
    if mol_most_similars:
        w = Chem.SDWriter(output)
        n_mol_found = 0
        for m in mol_most_similars: 
            w.write(m)
            n_mol_found += 1
        print("Number of found molecules {}".format(n_mol_found))
        #p = Pool(processes=20)
        #data = p.map(partial(search_most_similars, molecule_query=molecule_query, n_structs=n_structs), molecules_db) 
    return n_mol_found



def add_args(parser):
    parser.add_argument('database', type=str, help="database to query")
    parser.add_argument('molecules', nargs="+", help="molecule to query")
    parser.add_argument('--n', type=int, help="Number of structures tp retrieve", default=500)
    parser.add_argument('--tresh', type=float, help="Tanymoto similarity tresholt default=0.7", default=0.7)
    parser.add_argument('--output', type=str, help="Name of output file", default="analogs.sdf")
    parser.add_argument('--sb', action="store_true", help="Get the n most similar structs")
    parser.add_argument('--substructure', action="store_true", help="Get all the structures with a certain substructure")
    parser.add_argument('--combi_subsearch', action="store_true", help="Get almost on of the substructures in each sdf file")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Build 2D QSAR model')
    add_args(parser)
    args = parser.parse_args()
    query_database(args.database, args.molecules, n_structs=args.n, most_similars=args.sb, 
          combi_subsearch=args.combi_subsearch, substructure=args.substructure, output=args.output, treshold=args.tresh)
