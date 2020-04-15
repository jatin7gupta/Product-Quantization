from scipy.spatial import distance
from collections import defaultdict
import numpy as np


def pq(data, P, init_centroids, max_iter):
    # constant variables
    ROW_LENGTH, COL_LENGTH = data.shape
    CODE_BOOK_NUMBER, K, SUB_VECTOR_DIMS_SIZE = init_centroids.shape

    # dividing dimensions of data into p parts (M/P from spec)
    size_of_division = COL_LENGTH // P
    codebook = np.zeros((ROW_LENGTH, K))

    # key: cluster number
    # value: cluster points in key cluster
    cluster = defaultdict(list)
    for index in range(0, COL_LENGTH, size_of_division):
        # To get P as centroid index
        codebook_index = index//size_of_division

        # using l1 distance as cityblock
        codebook += distance.cdist(data[:, index:index+size_of_division], init_centroids[codebook_index], 'cityblock')

    for idx, value in enumerate(np.argmin(codebook, axis=1)):
        cluster[value].append(idx)

    for cluster_key, data_points in cluster.items():
        for index in range(0, COL_LENGTH, size_of_division):
            codebook_index = index // size_of_division
            init_centroids[codebook_index][cluster_key]  = np.mean(data[data_points, index:index+size_of_division], axis=0)


def query(queries, codebooks, codes, T):
    pass
