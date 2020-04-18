import heapq
import time
from queue import PriorityQueue

def heapsort(iterable):
    h = []
    for key ,value in enumerate(iterable):
        heapq.heappush(h, value)
    while len(h) > 0:
        heapq.heappop(h)

def pq(iterable):
    q = PriorityQueue()
    for key, val in enumerate(iterable):
        q.put((key, val))
    while not q.empty():
        next_item = q.get()





# generate random floating point values
from random import seed
from random import random
# seed random number generator
seed(1)
# generate random numbers between 0-1
l=[]

for _ in range(1000000):
    value = random()
    l.append(value)
start = time.time()
heapsort(l)
end = time.time()
print(end - start)

start = time.time()
pq(l)
end = time.time()
print(end - start)