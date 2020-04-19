from scipy.spatial import distance
from collections import defaultdict
import numpy as np
import heapq
import itertools



def pq(data, P, init_centroids, max_iter):
    # constant variables
    ROW_LENGTH, COL_LENGTH = data.shape
    CODE_BOOK_NUMBER, K, SUB_VECTOR_DIMS_SIZE = init_centroids.shape

    # dividing dimensions of data into p parts (M/P from spec)
    size_of_division = COL_LENGTH // P
    codebook_distance_sum = np.zeros((ROW_LENGTH, K))

    # key: cluster number
    # value: cluster points in key cluster
    cluster_list = None
    while max_iter > 0:
        cluster_list = list()
        codebook_distance_sum = np.zeros((ROW_LENGTH, K))

        for index in range(0, COL_LENGTH, size_of_division):
            # To get P as centroid index
            codebook_index = index//size_of_division
            cluster_list.append(defaultdict(list))
            # using l1 distance as cityblock
            dat = data[:, index:index+size_of_division]
            centroid = init_centroids[codebook_index]
            codebook_distance_sum = distance.cdist(dat, centroid, 'cityblock')

            for idx, value in enumerate(np.argmin(codebook_distance_sum, axis=1)):
                cluster_list[codebook_index][value].append(idx)

        for codebook_index in range(0, len(cluster_list)):
            cluster = cluster_list[codebook_index]
            # for index in range(0, COL_LENGTH, size_of_division):
            for cluster_key, data_points in cluster.items():

                # codebook_index = index // size_of_division
                # dat = data[data_points, index:index+size_of_division]
                ind = codebook_index * size_of_division
                dat = data[data_points, ind:ind + size_of_division]
                med = np.median(dat, axis=0)
                init_centroids[codebook_index][cluster_key] = med

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
    multi_index_list = []
    CLUSTER_NUMBER = 0
    DISTANCE = 1

    # creating P clusters depecting
    subvectors_clusters=[]
    for i in range(DIVISIONS):
        subvectors_clusters.append(defaultdict(list))
        multi_index_list.append(list())

    for data_index, points in enumerate(codes):
        for point_index, point in enumerate(points):
            subvectors_clusters[point_index][point].append(data_index)

    for q in queries:
        # creating result set
        result_set = set()

        # break the queries into sub vectors
        for index in range(0, COL_LENGTH, SUB_VECTOR_DIMS_SIZE):
            codebook_index = index // SUB_VECTOR_DIMS_SIZE

            # using l1 distance as cityblock
            # codebook_distance_sum = distance.cdist(codebooks[codebook_index],q[index:index + SUB_VECTOR_DIMS_SIZE],
            #                                         'cityblock')
            dist = (abs(q[index:index + SUB_VECTOR_DIMS_SIZE] - codebooks[codebook_index]))
            distance_subquery_codebooks = np.sum(dist, axis=1)
            for centroid_number, distance in enumerate(distance_subquery_codebooks):
                multi_index_list[codebook_index].append((centroid_number, distance))

        # sort multi_index_list
        for l in multi_index_list:
            l.sort(key=lambda x: x[DISTANCE])

        # this set will contain tuples which were added in the set for no duplication. (dedup)
        previous_occur = set()
        while len(result_set) < T:

            # take all zeros at once
            sum_of_distances = 0
            min_cluster_value = []
            for idx, index_list in enumerate(multi_index_list):
                top_row = index_list[0]
                sum_of_distances += top_row[DISTANCE]
                min_cluster_value.append((idx, top_row[CLUSTER_NUMBER]))

            for codebook_number, cluster_number in min_cluster_value:
                for data_points in subvectors_clusters[codebook_number][cluster_number]:
                    result_set.add(data_points)


            # for idx, index_list in enumerate(multi_index_list):
            #     table = itertools.product([0, 1], repeat=len(multi_index_list)-1)

        # adding result set to the result list
        result_list.append(result_set)
    return result_list
