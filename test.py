import submission
import pickle
import time

# How to run your implementation for Part 1
with open('./toy_example/Data_File', 'rb') as f:
    Data_File = pickle.load(f, encoding = 'bytes')
with open('./toy_example/Centroids_File', 'rb') as f:
    Centroids_File = pickle.load(f, encoding = 'bytes')
# l=[]
# import numpy as np
# Centroids_File = np.load('Test/Test_Case_2_Cent.npy')
# Data_File = np.load('Test/Test_Case_2.npy')
# for i in range(100):
start = time.time()
codebooks, codes = submission.pq(Data_File, P=2, init_centroids=Centroids_File, max_iter = 20)
end = time.time()
time_cost_1 = end - start
#     l.append(time_cost_1)
# print(sum(l)/len(l))
# print(f'min={min(l)}')
# print(f'max={max(l)}')
# print(codebooks)
# print(codes)


# How to run your implementation for Part 2
with open('./toy_example/Query_File', 'rb') as f:
    queries = pickle.load(f, encoding = 'bytes')
start = time.time()
candidates = submission.query(queries, codebooks, codes, T=10)
end = time.time()
time_cost_2 = end - start

# output for part 2.
# print(candidates)
