from analogs_finder.analysis import analysis_dataset as an
import types
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
from analogs_finder.search_methods import loader as ld
from analogs_finder.helpers import postfilter as pt
from analogs_finder.helpers import helpers as hp



def query_database(database, molecules, n_structs=500, combi_subsearch=False, most_similars=False, substructure=False, output="similars.sdf", hybrid=None, treshold=0.7, avoid_repetition=False, fp_type="DL", turbo=False, neighbours=5, analysis_dataset=False, test=False, dim_type="pca", atoms_to_grow=[], atoms_to_avoid=[], only_postfilter=False):

    #Initial checks
    assert type(database) == str, "database must be a unique sdf file"
    assert type(molecules) == list, "query molecule must be a list of a single or multiple sdf files"

    # Set tanimoto threshold and fp type
    if type(treshold) == list and type(fp_type) == list:
        if len(treshold) == 1 and len(fp_type) == 1:
           treshold = treshold[0]
           fp_type = fp_type[0] 

    # Load database
    molecules_db= Chem.SDMolSupplier(database)

    # Perform database analysis
    if analysis_dataset:
        print("Analysing dataset...")
        molecule_query = next(Chem.SDMolSupplier(molecules[0]))
        an.main(molecule_query, molecules_db, test=test, dim_type=dim_type)
        return

    # Load query molecule
    molecule_query = ld.load_query_molecule(molecules, most_similars, turbo,
            combi_subsearch, substructure, hybrid, treshold, fp_type, only_postfilter) 

    # Load method to use
    mol_most_similars = ld.load_method_to_use(most_similars, turbo, substructure, combi_subsearch,
        hybrid, fp_type, treshold, n_structs, molecule_query, molecules_db, neighbours,
        only_postfilter)

    #If output
    if mol_most_similars:
        mol_most_similars = list(mol_most_similars)

        #Write molecules before filtering
        n_mol_found_before_filter = hp.molecules_to_sdf(mol_most_similars, "before_filter_" + output)
        print("Number of found molecules {} before filter".format(n_mol_found_before_filter))

        #Filter molecules
        mols_after_filter = pt.postfilter_mols(molecule_query, mol_most_similars, atoms_to_grow, atoms_to_avoid, avoid_repetition)

        #Write molecules after filtering
        n_mol_found_after_filter = hp.molecules_to_sdf(mols_after_filter, output)
        print("Number of found molecules {} after filter".format(n_mol_found_after_filter))
        #p = Pool(processes=20)
        #data = p.map(partial(search_most_similars, molecule_query=molecule_query, n_structs=n_structs), molecules_db) 
    return n_mol_found_after_filter


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
    parser.add_argument('--turbo', action="store_true", help="Run similarity for your reference structure and N most similar neighbours")
    parser.add_argument('--neighbours', type=int, help="Number of neighbours in turbo search. Ignored if not flag --turbo")
    parser.add_argument('--analysis_dataset', action="store_true", help="Retrieve the similarity distribution of your dataset")
    parser.add_argument('--test', action="store_true", help="Whether to run test or not")
    parser.add_argument('--dim_type', type=str, help="Dimensionallity reduction mothod to use when analyzing", default="pca")
    parser.add_argument('--atoms_to_grow', nargs="+", type=int, help="Atoms you want to grow towards", default=[])
    parser.add_argument('--atoms_to_avoid', nargs="+", type=int, help="Atoms you want to avoid growing to", default=[])
    parser.add_argument('--only_postfilter', action="store_true", help="Postfilter results from a previous analog search")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Find analogs to a query molecule on your private database')
    add_args(parser)
    args = parser.parse_args()
    query_database(args.database, args.molecules, n_structs=args.n, most_similars=args.sb, 
          combi_subsearch=args.combi_subsearch, substructure=args.substructure, output=args.output, treshold=args.tresh, avoid_repetition=args.avoid_repetition, hybrid=args.hybrid, fp_type=args.fp_type, turbo=args.turbo, neighbours=args.neighbours, analysis_dataset=args.analysis_dataset, test=args.test, dim_type=args.dim_type, atoms_to_grow=args.atoms_to_grow, atoms_to_avoid=args.atoms_to_avoid, only_postfilter=args.only_postfilter)
