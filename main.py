import os
import argparse
import random as rand
from oram import Oram
from oram import Ring
from path import Path
from path import PaInf
import numpy as np
import math
import sys
import csv
# from memory_profiler import profile


def record_data(f, counts):
    data = [counts]
    with open(f, 'w') as csvfile:
        writer=csv.writer(csvfile, delimiter="\t")
        writer.writerows(data)


def access_n(oram, stash_sizes, full_buckets, occupancies, rounds=1, z=1):
    for i in range(rounds):
        print("Accessing 1 through n round ", i)
        for j in range(1,oram.n+1):
            oram.access(j)
            current_size = len(oram.buckets[0])
            stash_sizes[current_size] += 1
            stats = oram.get_stats()
            full_buckets = np.append(full_buckets, [stats[0]], axis=0)
            occupancies = np.append(occupancies, [stats[1]], axis=0)
            # s,d = oram.max_rooted_subtree_size_and_depth(z)
            # full_sizes[s] += 1
            # if s>0:
                # full_depths[d] += 1
    return (stash_sizes, full_buckets, occupancies)
        # oram.print_occupancies()

def init_painf(l, z, n=None):
    pinf = PaInf(l,z,n)
    pinf.init_pos_map()
    pinf.init_tree()
    for i in range(1,n+1):
        pinf.access(i)
    counts = [0] * (pinf.n+1)
    return (pinf, counts)

def init_path(l, z, n = None):
    path = Path(l, z, n)
    path.init_pos_map()
    path.init_tree()
    for i in range(1,n+1):
        path.access(i)
    print("initialized!")
    counts = [0] * (path.n+1)
    full_buckets = np.array([[0]*(l+1)], dtype=np.dtype('u2'))
    occupancies = np.array([[0]*(l+1)], dtype=np.dtype('u2'))
    return (path, counts, full_buckets, occupancies)

# levels are 0,..l
# total number of buckets in tree is 2**(l+1)-1
# distinct real blocks are 0,...,a*(2**(l-1))
# eviction rate for ring is a (allowed to approach 2z)
# need s-a around 3-5
def init_ring(l, a, s, z):
    oram = Ring(l, a, s, z)
    oram.init_pos_map()
    oram.init_tree()
    oram.init_evict_order()
    for i in range(2**oram.l):
        oram.evict()
    print("initialized!")
    counts = [0] * (oram.n+1)
    return (oram, counts)


p = init_path(5, 3, 2**6)
counts = p[1]
full_buckets = p[2]
occupancies = p[3]
p = p[0]
res = access_n(p, counts, full_buckets, occupancies)
np.std(res[1],axis=0)
np.mean(res[1], axis=0)
>>> np.delete(res[1],[0]*6,axis=0)
