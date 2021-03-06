from scipy.spatial import distance
from collections import defaultdict
import numpy as np
import heapq
import itertools


def pq(data, P, init_centroids, max_iter):
    # constant variables
    ROW_LENGTH, COL_LENGTH = data.shape

    # dividing dimensions of data into p parts (M/P from spec)
    size_of_division = COL_LENGTH // P

    # key: cluster number
    # value: cluster points in key cluster
    cluster_list = None
    while max_iter > 0:
        cluster_list = list()

        for index in range(0, COL_LENGTH, size_of_division):
            # To get P as centroid index
            codebook_index = index//size_of_division
            cluster_list.append(defaultdict(list))

            # using l1 distance as cityblock
            codebook_distance_sum = distance.cdist(data[:, index:index+size_of_division], init_centroids[codebook_index], 'cityblock')

            # getting the minimum distance for each data point from each cluster point
            for idx, value in enumerate(np.argmin(codebook_distance_sum, axis=1)):
                cluster_list[codebook_index][value].append(idx)

        for codebook_index in range(0, len(cluster_list)):
            for cluster_key, data_points in cluster_list[codebook_index].items():
                # using medians to get the next centroid
                ind = codebook_index * size_of_division
                init_centroids[codebook_index][cluster_key] = \
                    np.median(data[data_points, ind:ind + size_of_division], axis=0)

        max_iter = max_iter-1

    # calculating codes
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
    CENTROID_NUMBER = 0
    DISTANCE = 1

    # creating P clusters depecting
    subvectors_clusters = defaultdict(list)

    for data_index, points in enumerate(codes):
        subvectors_clusters[tuple(points)].append(data_index)

    for q in queries:
        multi_index_list = create_multi_index_list(DIVISIONS)

        # creating result set for each query
        result_set = set()

        # break the queries into sub vectors
        for index in range(0, COL_LENGTH, SUB_VECTOR_DIMS_SIZE):
            codebook_index = index // SUB_VECTOR_DIMS_SIZE

            # using l1 distance as cityblock
            dist = (abs(q[index:index + SUB_VECTOR_DIMS_SIZE] - codebooks[codebook_index]))
            distance_subquery_codebooks = np.sum(dist, axis=1)
            for centroid_number, distance in enumerate(distance_subquery_codebooks):
                multi_index_list[codebook_index].append((centroid_number, distance))

        # sort multi_index_list on distance
        for l in multi_index_list:
            l.sort(key=lambda x: x[DISTANCE])

        base_list = [0] * len(multi_index_list)
        heap = []

        dedup_set = set()

        # init get first row of all tables
        centriod_key, distance_centroid_query = get_smallest_centroid_datapoints(
            CENTROID_NUMBER, DISTANCE, base_list,multi_index_list)

        # add init node to heap and dedup_set
        tuple_centriod_key = tuple(centriod_key)
        tuple_index_key = tuple(base_list)
        dedup_set.add(tuple_index_key)
        heapq.heappush(heap, Node(distance_centroid_query, tuple_centriod_key, tuple_index_key))

        # stencil_matrix helps in finding nearest neighbours
        stencil_matrix = []
        for idx, val in enumerate(base_list):
            new_list = list(base_list)
            new_list[idx] = new_list[idx] + 1
            stencil_matrix.append(new_list)
            
        def adder(a, b):
            return a + b

        while len(result_set) < T and len(heap) > 0:
            # get the top value form the top
            node = heapq.heappop(heap)
            centroid_number_tuple = node.centroid_number_tuple
            centroid_index_tuple = node.centroid_index_tuple

            # add results to the set
            for data_point in subvectors_clusters[centroid_number_tuple]:
                result_set.add(data_point)

            # stop if we found the nearest neighbours
            if len(result_set) >= T:
                break

            # getting all nearest neighbours, checking duplicates(dedup) and adding in heap
            for e in stencil_matrix:
                one_step_ahead = map(adder, e, centroid_index_tuple)

                # check for dedup
                one_step_ahead = tuple(one_step_ahead)
                if one_step_ahead not in dedup_set:

                    # get the value for heap
                    centriod_key, distance_centroid_query = get_smallest_centroid_datapoints(
                        CENTROID_NUMBER, DISTANCE, one_step_ahead, multi_index_list)
                    if centriod_key is not None and distance_centroid_query is not None:
                        # added to dedup set
                        dedup_set.add(one_step_ahead)

                        # add new node to heap
                        tuple_centriod_key = tuple(centriod_key)
                        dedup_set.add(one_step_ahead)
                        heapq.heappush(heap, Node(distance_centroid_query, tuple_centriod_key, one_step_ahead))

        # adding result set to the result list
        result_list.append(result_set)
    return result_list


def create_multi_index_list(DIVISIONS: int):
    mi_list = list()
    for i in range(DIVISIONS):
        mi_list.append(list())
    return mi_list


def get_smallest_centroid_datapoints(CENTROID_NUMBER, DISTANCE, base_list, multi_index_list):
    # centriod_key can be change
    centriod_key = []
    distance_centroid_query = 0
    try:
        for idx, cluster_point in enumerate(base_list):
            tuple_centriod_number_distance = multi_index_list[idx][cluster_point]
            distance_centroid_query += tuple_centriod_number_distance[DISTANCE]
            centriod_key.append(tuple_centriod_number_distance[CENTROID_NUMBER])
        return centriod_key, distance_centroid_query
    except:
        return None, None


class Node(object):
    def __init__(self, dist: int, centroid_number_tuple: tuple, centroid_index_tuple: tuple):
        self.dist = dist
        self.centroid_number_tuple = centroid_number_tuple
        self.centroid_index_tuple = centroid_index_tuple

    def __lt__(self, other):
        return self.dist < other.dist