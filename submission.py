from scipy.spatial import distance
from collections import defaultdict
import numpy as np


def pq(data, P, init_centroids, max_iter):
    # constant variables
    ROW_LENGTH, COL_LENGTH = data.shape
    CODE_BOOK_NUMBER, K, SUB_VECTOR_DIMS_SIZE = init_centroids.shape

    # dividing dimensions of data into p parts (M/P from spec)
    size_of_division = COL_LENGTH // P
    codebook_distance_sum = np.zeros((ROW_LENGTH, K))

    # key: cluster number
    # value: cluster points in key cluster
    cluster = None
    while max_iter > 0:
        cluster = defaultdict(list)
        codebook_distance_sum = np.zeros((ROW_LENGTH, K))

        for index in range(0, COL_LENGTH, size_of_division):
            # To get P as centroid index
            codebook_index = index//size_of_division

            # using l1 distance as cityblock
            codebook_distance_sum += distance.cdist(data[:, index:index+size_of_division], init_centroids[codebook_index], 'cityblock')

        for idx, value in enumerate(np.argmin(codebook_distance_sum, axis=1)):
            cluster[value].append(idx)

        for cluster_key, data_points in cluster.items():
            for index in range(0, COL_LENGTH, size_of_division):
                codebook_index = index // size_of_division
                init_centroids[codebook_index][cluster_key] = \
                    np.median(data[data_points, index:index+size_of_division], axis=0)

        max_iter = max_iter-1
    # TODO: maybe we have to calculate once again
    codes = None
    first_time = True
    for index in range(0, COL_LENGTH, size_of_division):
        # To get P as centroid index
        codebook_index = index // size_of_division

        # using l1 distance as cityblock
        codes_distances = distance.cdist(data[:, index:index + size_of_division], init_centroids[codebook_index],
                                         'cityblock')
        if first_time:
            codes = np.argmin(codes_distances, axis=1)
            first_time = False
        else:
            codes = np.column_stack((codes, np.argmin(codes_distances, axis=1)))
    return init_centroids, codes.astype(np.uint8)


def query(queries, codebooks, codes, T):
    # final result list
    result_list = []
    QUERIES_COUNT, COL_LENGTH = queries.shape
    NUMBER_OF_DATA_POINTS, DIVISIONS = codes.shape
    CODE_BOOK_NUMBER, K, SUB_VECTOR_DIMS_SIZE = codebooks.shape

    # creating P clusters depecting
    subvectors_clusters=[]
    for i in range(DIVISIONS):
        subvectors_clusters.append(defaultdict(list))

    for data_index, points in enumerate(codes):
        for point_index, point in enumerate(points):
            subvectors_clusters[point_index][point].append(data_index)


    for q in queries:
        # creating result set
        result_set = set()

        distance_centriod_query = []
        # break the queries into sub vectors
        for index in range(0, COL_LENGTH, SUB_VECTOR_DIMS_SIZE):
            codebook_index = index // SUB_VECTOR_DIMS_SIZE

            # using l1 distance as cityblock
            # codebook_distance_sum = distance.cdist(codebooks[codebook_index],q[index:index + SUB_VECTOR_DIMS_SIZE],
            #                                         'cityblock')
            dist = (abs(q[index:index + SUB_VECTOR_DIMS_SIZE] - codebooks[codebook_index]))
            distance_centriod_query.append(np.sum(dist, axis=1))
            x=2

        # adding result set to the result list
        result_list.append(result_set)
