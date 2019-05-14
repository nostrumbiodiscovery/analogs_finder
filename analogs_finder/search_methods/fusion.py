from analogs_finder.search_methods import methods as mt
from analogs_finder.search_methods import molecule as ml
from analogs_finder.search_methods import similarity as sm



def turbo_similarity(mref, molecules, neighbours=5, treshold=0.7, fp_type="DL"):
    """
    Turbo similarity searching uses information 
    about the nearest neighbors in a conventional 
    chemical similarity search to increase the 
    effectiveness of virtual screening with a data 
    fusion approach being used to combine the 
    nearest neighbor information. 
    Paper: https://onlinelibrary.wiley.com/doi/abs/10.1002/sam.10037
    """
    mol_most_similars  = mt.search_most_similars(mref, molecules, neighbours, fp_type=fp_type)
    mol_most_similars.insert(0, ml.Molecule(mref))
    molecules_ref = [ m.molecule for m in mol_most_similars ]
    for m in sm.compute_similarity_several_mols(molecules_ref, molecules, fp_type=fp_type):
        if any(s > float(treshold) for s in m.similarities):
            sim_min = min(m.similarities)
            m.molecule.SetProp("Similarity", "{}".format(sim_min))
            yield m
        else:
            pass
