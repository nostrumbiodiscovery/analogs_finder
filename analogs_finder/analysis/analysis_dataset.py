import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from rdkit import DataStructs
from analogs_finder.analysis import plot as pt
from analogs_finder.search_methods import similarity as sim
from analogs_finder.search_methods import molecule as ml
from analogs_finder.analysis import dimensionallity as dm


def main(molecule_query, molecules_db, n_bins=100, fp_types=["DL", "MACCS", "circular"], test=None, dim_type="umap"):

    #Analysis code
    for fp_type in fp_types:

        # Retrieve fingerprints and similarity for analysis
        counts = []
        svg = [None] * 100
        fp = [None] * 100
        similarity = [0] * 100
        for m in tqdm(sim.compute_similarity(molecule_query, molecules_db, fp_type)):
            #Build similarity counts
            counts_step, bins = pt.histogram(m.similarity, n_bins=n_bins)
            counts = np.add(counts, counts_step) if len(counts) != 0 else counts_step

            #Build fingeprints
            idx = np.argmin(similarity)
            less_similar = similarity[idx]
            if m.similarity > less_similar:
                fp[idx] = m.fp
                similarity[idx] = m.similarity
                svg[idx] = m.to_svg()

        #Plot similarity distribution
        if not test:
            fig, ax = plt.subplots()
            ax.hist(bins[1:], bins, weights=counts)
            plt.savefig("similarity_hist_{}.png".format(fp_type))

        #Retrieve similarity distribution data
        values = np.vstack([bins[1:], counts]).T
        np.savetxt("counts_{}.txt".format(fp_type), values,  fmt=['%f','%d'])

        if fp_type == "circular":
            #Add reference molecule
            mref = ml.molec_properties(molecule_query, fp_type=fp_type)
            fp.insert(0, mref.fp)
            similarity.insert(0, 1)
            svg.insert(0, mref.to_svg())

            #Clean results
            svg = [ value for value in svg if value ]
            fp = [ value for value in fp if value ]
            similarity = [ value for value in similarity if value!= 0 ]

            #Reduce Dimension
            X = np.asarray([ fp2arr(f) for f in fp ])
            embedding = dm.ReduceDimension(X, 2).run(dim_type)

            #Plot Reduce Dimension graph
            if not test:
                pt.interactive_map(embedding[:, 0], embedding[:, 1], svg, color=np.array(similarity))

def fp2arr(fp):
    arr = np.zeros((1,))
    DataStructs.ConvertToNumpyArray(fp,arr)
    return arr

