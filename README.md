
# Product Quantization using Inverted multi-index

### Product Quantization

This project implements a product quantization-based approach for approximate nearest neighbor search. The idea is to decompose the space into a Cartesian product of low-dimensional subspaces and to quantize each subspace separately. A vector is represented by a short code composed of its subspace quantization indices. The L1 (manhattan) distance between two vectors can be efficiently estimated from their codes. An asymmetric version increases precision, as it computes the approximate distance between a vector and a code. Experimental results show that this approach searches for nearest neighbors efficiently, in particular in combination with an inverted file system. Results for SIFT and GIST image descriptors show excellent search accuracy, outperforming three stateof-the-art approaches. The scalability of our approach is validated on a data set of two billion vectors.

### Inverted multi-index
A new data structure for efﬁcient similarity search in very large datasets of high-dimensional vectors is implemented. This structure called the inverted multi-index generalizes the inverted index idea by replacing the standard quantization within inverted indices with product quantization. For very similar retrieval complexity and pre-processing time, inverted multi-indices achieve a much denser subdivision of the search space compared to inverted indices, while retaining their memory efﬁciency. Experiments with large datasets of SIFT and GIST vectors demonstrate that because of the denser subdivision, inverted multi-indices are able to return much shorter candidate lists with higher recall, according to the research given below. Augmented with a suitable reranking procedure, multi-indices were able to signiﬁcantly improve the speed of approximate nearest neighbor search on the dataset of 1 billion SIFT vectors compared to the best previously published systems, while achieving better recall and incurring only few percent of memory overhead.



## Requirements
 * **Scipy 1.4.1**
 * **Numpy 1.18.2**
 * **Python 3.6**

## Installation steps
1. You have to be in the root of the project to follow the below steps. i.e. venv should be in the root of the folder.
2. Make a new virtual environment for python.

```bash
$ python -m venv ./venv
```

3. Activate virtual environment. <br/>
   Windows | Linux/Mac

```bash
$ venv\Scripts\activate.bat | $ source ./venv/bin/activate
```

4. Install requirements.

```bash
$ pip install -r requirements.txt
```

# Part1: PQ for L1 Distance 

1. **data** is an array with shape (N,M) and dtype='float32', where N is the number of vectors and M is the dimensionality.
2. **P** is the number of partitions/blocks the vector will be split into. Note that in the examples from the inverted multi index paper, P is set to 2. But in this project, you are required to implement a more general case where P can be any integer >= 2. You can assume that P is always divides M in this project. 
3. **init_centroids** is an array with shape (P,K,M/P) and dtype='float32', which corresponds to the initial centroids for P blocks. For each block, K M/P-dim vectors are used as the initial centroids. **Note** that in this project, K is fixed to be 256.
4. **max_iter** is the maximum number of iterations of the K-means* clustering algorithm. **Note** that in this project, the stopping condition of K-means* clustering is that the algorithm has run for ```max_iter``` iterations.

## Return Format (Part 1)

The `pq()` method returns a codebook and codes for the data vectors, where
* **codebooks** is an array with shape (P, K, M/P) and dtype='float32', which corresponds to the PQ codebooks for the inverted multi-index. E.g., there are P codebooks and each one has K M/P-dimensional codewords.
* **codes** is an array with shape (N, P) and dtype=='uint8', which corresponds to the codes for the data vectors. The dtype='uint8' is because K is fixed to be 256 thus the codes should integers between 0 and 255. 

## Implementation details
Each datapoint is partitioned P times to get sub-vectors. The idea is to find the cluster point which is closest to the sub-vector using Manhattan distance (L1/’cityblock’). Running that for all sub-vectors gives us the information of which cluster centroid represents which points. Once a sub-vector is assigned a cluster, the cluster center changes so as to best represent the vectors that belong in it. New cluster center is calculated by taking median of all the member sub-vectors. We chose L1-norm because the L2 norm squares values, so it increases the cost of outliers exponentially; the L1 norm only takes the absolute value, so it considers them linearly. The exponentiation amplifies the effect of outliers. This entire process is run for a maximum of ‘max_iter’ iterations which is provided with input. At the end, we get our codebooks with values(maybe different from initial values) which will be used to calculate the codes.

Codes is the information of sub-vectors and shows which cluster the sub-vector belongs to. Values are obtained by running the above process once and store the centroid index which is closest to the sub-vector. Codes are returned as ‘uint8’ data type along with the codebooks.


# Part2: Query using Inverted Multi-index with L1 Distance


1. **queries** is an array with shape (Q, M) and dtype='float32', where Q is the number of query vectors and M is the dimensionality.
2. **codebooks** is an array with shape (P, K, M/P) and dtype='float32', which corresponds to the `codebooks` returned by `pq()` in part 1.
3. **codes** is an array with shape (N, P) and dtype=='uint8', which corresponds to the `codes` returned by `pq()` in part 1.
4. **T** is an integer which indicates the minimum number of returned candidates for each query. 

## Return Format (Part 2)

The `query()` method returns an array contains the candidates for each query. Specifically, it returns
* **candidates** is a list with Q elements, where the i-th element is a **set** that contains at least T integers, corresponds to the id of the candidates of the i-th query. For example, assume T=10, for some query we have already obtained 9 candidate points. Since 9 < T, the algorithm continues. Assume the next retrieved cell contains 3 points, then the returned set will contain 12 points in total.

## Implementation details
Part 2 implements the query method using inverted multi-index list with L1-norm. The objective is to query the codebook and obtain at least T candidates for each query. A multi-index list for each query is maintained that stores the distance of the query from the corresponding centroids. The distance is Manhattan distance(L1/’cityblock’) as per the reasons mentioned above. This list is sorted in ascending order of distance to get the centroid that is closest to the query. We also maintain a ‘subvectors_clusters’ python dictionary whose key is the tuple of centroids and value is the data points that belong to these centroids calculated from codes.

For algorithm 3.1, the closest combination of centroids is chosen to get the candidates. In order to prevent repetition of combination, a ‘dedup’  set is maintained. We maintain a stencil matrix so as to systematically navigate and pick the next combination of closest centroids. A min-Heap of Nodes (complex object) is maintained to always fetch the minimum farthest combination of centroid. Node is a custom Data Structure that stores the combinations centroids for all sub-vectors of query and the respective sum of distance. This structure exists simply to aide in retrieval of combination(centroid indexes) and distance. Each navigation lands us to a new combination and we add it to the heap. The min-Heap is sorted in ascending order hence the smallest element on the basis of distance (which we want) is the first element. Should the combination not exist in ‘dedup’ set, then it is added and we look up ‘subvectors_clusters’ to get the member data points. A spread, which we define as the point from which we need to start looking at the next closest combination. The closest point of one iteration becomes the new point of spread from where we navigate along one step in each dimension (maintained via stencil matrix). This process of finding the closest centroid combination (and consequently the data points) is performed till we have at least ‘T’ data points per query. The process boils down to finding the members of the cluster the query point belongs to. Should the result be less than ‘T’ candidates then we go for the next best cluster(closest cluster) and get its data points. 


## How to run implementation (Example)


```python
import submission
import pickle
import time

# How to run your implementation for Part 1
with open('./toy_example/Data_File', 'rb') as f:
    Data_File = pickle.load(f, encoding = 'bytes')
with open('./toy_example/Centroids_File', 'rb') as f:
    Centroids_File = pickle.load(f, encoding = 'bytes')
start = time.time()
codebooks, codes = submission.pq(data, P=2, init_centroids=centroids, max_iter = 20)
end = time.time()
time_cost_1 = end - start


# How to run your implementation for Part 2
with open('./toy_example/Query_File', 'rb') as f:
    queries = pickle.load(f, encoding = 'bytes')
start = time.time()
candidates = submission.query(queries, codebooks, codes, T=10)
end = time.time()
time_cost_2 = end - start

# output for part 2.
print(candidates)
```




    [{3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14}]

#### Implementation and Algorithm sources:
1. **[Inverted Multi Index](./In_Multi-Index.pdf)** 
2. **[Product Quantization: N-Nearest Neighbour](./PQ%20NN.pdf)**

#### Purpose
To understand the algorithms and implement them. These algorithms are widely used in many Data Science packages. 

