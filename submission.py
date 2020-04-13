from scipy.spatial import distance
from collections import defaultdict
import numpy as np
def pq(data, P, init_centroids, max_iter):
    d = defaultdict(list)
    # constant variables
    ROW_LENGTH, COL_LENGTH = data.shape

    # dividing dimensions of data into p parts (M/P from spec)
    size_of_division = COL_LENGTH // P
    for index in range(0, COL_LENGTH, size_of_division):
        # To get P as centroid index
        centriod_index = index//size_of_division
        ans = distance.cdist(data[:, index:index+size_of_division], init_centroids[centriod_index], 'cityblock')
        print(np.argmin(ans, axis=1))
        for idx, value in enumerate(np.argmin(ans, axis=1)):
            d[value].append(idx)

        print(ans)


def query(queries, codebooks, codes, T):
    pass
