# import heapq
# import time
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
constructTT(divisions=4)