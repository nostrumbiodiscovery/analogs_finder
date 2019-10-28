from rdkit import Chem
from analogs_finder.search_methods import methods as mt
from analogs_finder.search_methods import fusion as fs
from analogs_finder.search_methods import molecule as ml



def load_query_molecule(molecules, most_similars, turbo, combi_subsearch, substructure, hybrid, treshold, fp_type, only_postfilter):
    if only_postfilter:
         molecule_query = next(Chem.SDMolSupplier(molecules[0]))
    elif most_similars:
        molecule_query = next(Chem.SDMolSupplier(molecules[0]))
    elif turbo:
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
    return molecule_query


def load_method_to_use(most_similars, turbo, substructure, combi_subsearch, 
        hybrid, fp_type, treshold, n_structs, molecule_query, molecules_db,
        neighbours, only_postfilter): 
    mol_most_similars = None
    if only_postfilter:
        mol_most_similars = [ml.Molecule(m) for m in molecules_db if m]
    elif most_similars:
        mol_most_similars  = mt.search_most_similars(molecule_query, molecules_db, n_structs, fp_type=fp_type)
    elif turbo:
        mol_most_similars = fs.turbo_similarity(molecule_query, molecules_db, neighbours=neighbours, treshold=treshold, fp_type=fp_type)
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
    return mol_most_similars
        
