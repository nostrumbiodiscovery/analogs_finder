
from rdkit import Chem

database = "database.sdf"
qmolecule = "substructre_1.sdf"

molecules_db= Chem.SDMolSupplier(database)
molecule_query = next(Chem.SDMolSupplier(qmolecule))


from analogs_finder.analysis import analysis_dataset as an


#Use Uniform manifold to plot the chemical space
an.main(molecule_query, molecules_db, dim_type="umap", test=True)

#Use PCA to plot the chemical space
an.main(molecule_query, molecules_db, dim_type="pca", test=True)


#Most similar N molecules
from analogs_finder.search_methods import methods as mt
from analogs_finder.helpers import helpers as hp

output = "most_similars.sdf"
n_structs = 50

similars  = mt.search_most_similars(molecule_query, molecules_db, n_structs)
similars_no_duplicates = hp.remove_duplicates(similars)

w = Chem.SDWriter(output)
for m in similars_no_duplicates: w.write(m.molecule)

#Tanimoto
treshold = 0.6

similars  = mt.search_similarity_tresh(molecule_query, molecules_db, treshold)
similars_no_duplicates = hp.remove_duplicates(similars)

w = Chem.SDWriter(output)
for m in similars_no_duplicates: w.write(m.molecule)

#Substructure search
substructures = "substructre_2.sdf"

molecule_query = Chem.SDMolSupplier(substructures)
similars  = mt.search_substructure(molecule_query, molecules_db)
similars_no_duplicates = hp.remove_duplicates(similars)

w = Chem.SDWriter(output)
for m in similars_no_duplicates: w.write(m.molecule)


#Combination Substructure search
import glob

substructures_sdf = glob.glob("subs*.sdf")

similars = mt.combi_substructure_search(substructures_sdf, molecules_db)
similars_no_duplicates = hp.remove_duplicates(similars)

w = Chem.SDWriter(output)
for m in similars_no_duplicates: w.write(m.molecule)

#Hybrid
substructure_file = "substructre_3.sdf"

similars = mt.most_similar_with_substructure(molecule_query, molecules_db, substructure_file, treshold=0.1)

w = Chem.SDWriter(output)
for m in similars_no_duplicates: w.write(m.molecule)

#Fingerprint types
molecule_query = next(Chem.SDMolSupplier("substructre_3.sdf"))
substructure_file = "substructure.sdf"

similars_daylight = mt.search_most_similars(molecule_query, molecules_db, 2, fp_type="DL")
similars_circular = mt.search_most_similars(molecule_query, molecules_db, 2, fp_type="circular")
similars_torsions = mt.search_most_similars(molecule_query, molecules_db, 2, fp_type="torsions")
similars_MACCS = mt.search_most_similars(molecule_query, molecules_db, 2, fp_type="MACCS")
similars_pharm = mt.search_most_similars(molecule_query, molecules_db, 2, fp_type="pharm")


#Use all fingerprint method
tresholds = [0.7, 0.4, 0.4, 0.6]
fp_types = ["DL", "circular", "torsions", "MACCS"]
similarts = mt.search_similarity_tresh_several_fp(molecule_query, molecules_db, tresholds=tresholds, fp_types=fp_types)

#Use turbosearch
import analogs_finder.search_methods.fusion as fs
turbo_similars = fs.turbo_similarity(molecule_query, molecules_db, neighbours=5, treshold=0.4, fp_type="circular")
