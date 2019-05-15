from sklearn.decomposition import PCA
import umap


class ReduceDimension(object):

    def __init__(self, data, n_components):
        self.data = data
        self.n_components = n_components

    def run(self, method):
        if method == "umap":
            return self.compute_umap()
        elif method == "pca":
            return self.compute_pca()

    def compute_pca(self):
        pca = PCA(n_components=self.n_components)
        return pca.fit_transform(self.data)

    def compute_umap(self, neighbors=5, min_dist=0.2):
        reducer = umap.UMAP(n_neighbors=neighbors, min_dist=min_dist)
        return reducer.fit_transform(self.data)
        

