import numpy as np
import umap
import matplotlib.pyplot as plt
import mpld3
from mpld3 import plugins

def histogram(point, interval=[0,1], n_bins=10):
    point = float(point)
    bins = np.linspace(interval[0], interval[1], num=n_bins)
    counts = [0] * (n_bins-1)
    for i in range(1, n_bins):
        if (point > bins[i-1]) and (point < bins[i]):
            counts[i-1] =+ 1
            break
        else:
            pass
    return counts, bins


def boxplot(X, title="Similarity box plot", output="box_plot.png"):
    fig1, ax1 = plt.subplots()
    ax1.set_title(title)
    ax1.boxplot(data)
    fig1.savefig(output)


def scatter_plot(X, Y, title="Scatter plot", output="scatter_plot.png"):
    fig1, ax1 = plt.subplots()
    ax1.set_title(title)
    ax1.scatter(X, Y)
    fig1.savefig(output)

def UMAP_plot(X, Y, neighbors=5, min_dist=0.2, title="Chamical Space plot", output="chemical_space_plot.png"):
    reducer = umap.UMAP(n_neighbors=neighbors, min_dist=min_dist)
    embedding = reducer.fit_transform(X)
    fig, ax = plt.subplots()
    ax.scatter(embedding[:, 0], embedding[:, 1])
    fig.gca().set_aspect('equal', 'datalim')
    ax.set_title(title)
    ax.legend()
    fig.savefig(output)
    return embedding

def interactive_map(x, y, svgs, color=None):
    fig, ax = plt.subplots()
    # Compute areas and colors
    if color is None:
        points = ax.scatter(x, y, c=color, alpha=0.75)
    else:
        points = ax.scatter(x, y, c=color, alpha=0.75, cmap="viridis")
    # This is key point for making tooltip!
    plt.colorbar(points)
    tooltip = plugins.PointHTMLTooltip(points, svgs)
    plugins.connect(fig, tooltip)
    mpld3.show(fig)
