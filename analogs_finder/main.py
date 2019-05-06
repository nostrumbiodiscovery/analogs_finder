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
from analogs_finder.helpers import helpers as hp



def query_database(database, molecules, n_structs=500, combi_subsearch=False, most_similars=False, substructure=False, output="similars.sdf", hybrid=None, treshold=0.7, avoid_repetition=False, fp_type="DL"):

    assert type(database) == str, "database must be a unique sdf file"
    assert type(molecules) == list, "query molecule must be a list of a single or multiple sdf files"

    if type(treshold) == list and type(fp_type) == list:
        if len(treshold) == 1 and len(fp_type) == 1:
           treshold = treshold[0]
           fp_type = fp_type[0] 

    # Database
    molecules_db= Chem.SDMolSupplier(database)

    # Query Molecule
    if most_similars:
        molecule_query = next(Chem.SDMolSupplier(molecules[0]))
    elif combi_subsearch:
        molecule_query = molecules
    elif substructure:
        molecule_query = Chem.SDMolSupplier(molecules[0])
    elif hybrid:
        molecule_query = next(Chem.SDMolSupplier(molecules[0]))
    elif type(treshold) == list and type(fp_type) == list:
        molecule_query = next(Chem.SDMolSupplier(molecules[0]))
    elif treshold:
        molecule_query = next(Chem.SDMolSupplier(molecules[0]))

    # Method to use
    mol_most_similars = None
    if most_similars:
        mol_most_similars  = mt.search_most_similars(molecule_query, molecules_db, n_structs, fp_type=fp_type)
    elif substructure:
        mol_most_similars  = mt.search_substructure(molecule_query, molecules_db)
    elif combi_subsearch:
        mol_most_similars = mt.combi_substructure_search(molecule_query, molecules_db) 
    elif hybrid and treshold:
        mol_most_similars = mt.most_similar_with_substructure(molecule_query, molecules_db, hybrid, treshold, fp_type=fp_type)
    elif type(treshold) == list and type(fp_type) == list:
        mol_most_similars = mt.search_similarity_tresh_several_fp(molecule_query, molecules_db, tresholds=treshold, fp_types=fp_type)
    elif treshold:
        mol_most_similars  = mt.search_similarity_tresh(molecule_query, molecules_db, treshold, fp_type=fp_type)
        

    if mol_most_similars:
        if avoid_repetition:
            mol_most_similars = hp.remove_duplicates(mol_most_similars)
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
    parser.add_argument('--tresh', nargs="+", help="Tanymoto similarity tresholt default=0.7", default=[0.7])
    parser.add_argument('--output', type=str, help="Name of output file", default="analogs.sdf")
    parser.add_argument('--sb', action="store_true", help="Get the n most similar structs")
    parser.add_argument('--substructure', action="store_true", help="Get all the structures with a certain substructure")
    parser.add_argument('--combi_subsearch', action="store_true", help="Get almost on of the substructures in each sdf file")
    parser.add_argument('--avoid_repetition', action="store_true", help="Allow to have the same molecule name several times in the final sdf file")
    parser.add_argument('--hybrid', type=str, help="Hybird model between similarity and substructure search")
    parser.add_argument('--fp_type', nargs="+", help="Fingerprint type to use [DL, circular, torsions, MACCS]", default=["DL"])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Find analogs to a query molecule on your private database')
    add_args(parser)
    args = parser.parse_args()
    query_database(args.database, args.molecules, n_structs=args.n, most_similars=args.sb, 
          combi_subsearch=args.combi_subsearch, substructure=args.substructure, output=args.output, treshold=args.tresh, avoid_repetition=args.avoid_repetition, hybrid=args.hybrid, fp_type=args.fp_type)
