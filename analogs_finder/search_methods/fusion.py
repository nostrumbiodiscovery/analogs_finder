from analogs_finder.search_methods import methods as mt



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
    mol_most_similars.insert(0, mref)
    for similarities, m in mt.compute_similarity_several_mols(mol_most_similars, molecules, fp_type=fp_type):
        if any(s > float(treshold) for s in similarities):
            sim_min = min(similarities)
            m.SetProp("Similarity", "{}".format(sim_min))
            yield m
        else:
            pass
