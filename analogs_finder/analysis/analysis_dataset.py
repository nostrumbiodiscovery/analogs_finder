import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from rdkit import DataStructs
from analogs_finder.analysis import plot as pt
from analogs_finder.search_methods import similarity as sim
from analogs_finder.search_methods import molecule as ml
from sklearn.decomposition import PCA


def main(molecule_query, molecules_db, n_bins=100, fp_types=["DL", "circular", "MACCS"], test=None):
    for fp_type in fp_types:
        counts = []
        svg = [None] * 100
        fp = [None] * 100
        similarity = [0] * 100
        for m in tqdm(sim.compute_similarity(molecule_query, molecules_db, fp_type)):
            #Build histogram counts
            counts_step, bins = pt.histogram(m.similarity, n_bins=n_bins)
            counts = np.add(counts, counts_step) if len(counts) != 0 else counts_step
            #Build chemical space
            idx = np.argmin(similarity)
            less_similar = similarity[idx]
            if m.similarity > less_similar:
                fp[idx] = m.fp
                similarity[idx] = m.similarity
                svg[idx] = m.to_svg()

        #Add reference molecule
        if fp_type == "circular":
            mref = ml.molec_properties(molecule_query, fp_type=fp_type)
            fp.insert(0, mref.fp)
            similarity.insert(0, 1)
            svg.insert(0, mref.to_svg())
            #Clean results
            svg = [ value for value in svg if value ]
            fp = [ value for value in fp if value ]
            similarity = [ value for value in similarity if value!= 0 ]
            #Plot graph
            X = np.asarray([ fp2arr(f) for f in fp ])
            pca = PCA(n_components=3)
            res = pca.fit_transform(X)
            if not test:
                pt.interactive_map(res[:, 0], res[:, 1], svg, color=np.array(similarity))

        #Plot and histogram data
        fig, ax = plt.subplots()
        ax.hist(bins[1:], bins, weights=counts)
        plt.savefig("similarity_hist_{}.png".format(fp_type))

        #Retrieve hist data
        values = np.vstack([bins[1:], counts]).T
        np.savetxt("counts_{}.txt".format(fp_type), values,  fmt=['%f','%d'])
        #embedding = pt.UMAP_plot(fp, similarity,  output="chemical_space_plot_{}.png".format(fp_type))
        #values = np.vstack([range(res.shape[1]), res]).T
        #np.savetxt("chemical_space_{}.txt".format(fp_type), values,  fmt=['%d', '%f','%d'])

def fp2arr(fp):
    arr = np.zeros((1,))
    DataStructs.ConvertToNumpyArray(fp,arr)
    return arr

