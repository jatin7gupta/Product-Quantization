# import heapq
import time
# from queue import PriorityQueue
import itertools
#
# def heapsort(iterable):
#     h = []
#     for key ,value in enumerate(iterable):
#         heapq.heappush(h, value)
#     while len(h) > 0:
#         heapq.heappop(h)
#
# def pq(iterable):
#     q = PriorityQueue()
#     for key, val in enumerate(iterable):
#         q.put((key, val))
#     while not q.empty():
#         next_item = q.get()
#
#
#
#
#
# # generate random floating point values
# from random import seed
# from random import random
# # seed random number generator
# seed(1)
# # generate random numbers between 0-1
# l=[]
#
# for _ in range(1000000):
#     value = random()
#     l.append(value)
# start = time.time()
# heapsort(l)
# end = time.time()
# print(end - start)
#
# start = time.time()
# pq(l)
# end = time.time()
# print(end - start)
import heapq

class Node(object):
    def __init__(self, val: int):
        self.val = val

    def __repr__(self):
        return f'Node value: {self.val}'

    def __lt__(self, other):
        return self.val < other.val
#
# heap = [Node(2), Node(0), Node(1), Node(4), Node(2)]
# s = set()
# heapq.heapify(heap)
# print(heap)  # output: [Node value: 0, Node value: 2, Node value: 1, Node value: 4, Node value: 2]
#
# s.add(heapq.heappop(heap))  # output: [Node value: 1, Node value: 2, Node value: 2, Node value: 4]
# s.add(heapq.heappop(heap))
# s.add(heapq.heappop(heap))
# s.add(heapq.heappop(heap))
# print(s)
# s = set()
#
# s.add((1,(1,2,3)))
# s.add((1,(1,2,3)))
# print(s)

# table = itertools.product([0, 1], repeat=1)
# for p in table:
#     print(p)

def addStringAtIndex(string_row:str, index: int):
    string_row = string_row[:index] + '0' + string_row[index:]
    return string_row

def stringTable(str_table: list, index: int):
    new_tab = list()
    for item in str_table:
        new_tab.append(addStringAtIndex(item, index))
    return new_tab

def constructTT(divisions: int):
    tru_table = list()
    table = [item for item in itertools.product([0, 1], repeat=divisions-1)]
    str_table = []

    for p in table:
        p = "".join(map(str, p))
        str_table.append(p)

    for i in range(divisions):
        tru_table.append(stringTable(str_table, i))

        # for tab in tru_table[i]:
        #     tab = addStringAtIndex(tab, i)
    for tab in tru_table:
        print(tab)

        # for t in tab:
        #     print(len(t))
    # print(tru_table)
# constructTT(divisions=3)

import numpy as np
# def myfunc(a, b):
#   return a + b
# x = map(myfunc, itertools.product([0, 1], repeat=2), [2,2])
# print(list(x))
# #
# start = time.time()
# for i in range(10000000):
#     l = []
#     for e in itertools.product([0, 1], repeat=2):
#         x = map(myfunc, e, (2, 2))
#         l.append(tuple(x))
# end = time.time()
# print(end - start)
#
#
# start = time.time()
# for i in range(10000000):
#
#     array = np.array([item for item in itertools.product([0, 1], repeat=2)])
#     array2 = np.array([2,2])
#     array+array2
# end = time.time()
# print(end - start)

# l  = 3
# for idx, val in enumerate(range(3)):
#     print(idx, val)
base = [0,0,0]
stencil_matrix =[]
for idx, val in enumerate(base):
    for idx_i, val_i in enumerate(itertools.product([0, 1], repeat=len(base)-1)):
        # tuple does not support insert, if this is expensive we will use slicing
        list_from_tuples = list(val_i)
        list_from_tuples.insert(idx, val)
        stencil_matrix.append(list_from_tuples)


def adder(a, b):
    return a + b


l = []
for e in stencil_matrix:
    # replace new smallest vector from heap in place of (0,1,1)
    x = map(adder, e, (0,0,0))
    l.append(tuple(x))
print(l)