import os
import argparse
import random as rand
from oram import Oram
from oram import Ring
from path import Path
from path import PaInf
import math
import sys
# from memory_profiler import profile



def access_n(oram, counts, rounds):
    for i in range(rounds):
        print("Accessing 1 through n round ", i)
        for j in range(1,oram.n+1):
            oram.access(j)
            current_size = len(oram.buckets[0])
            counts[current_size] += 1
        # oram.print_occupancies()


def init_path(l, z, n = None):
    path = Path(l, z, n)
    path.init_pos_map()
    path.init_tree()
    for i in range(1,n+1):
        path.access(i)
    print("initialized!")
    counts = [0] * (path.n+1)
    return (path, counts)

# levels are 0,..l
# total number of buckets in tree is 2**(l+1)-1
# distinct real blocks are 0,...,a*(2**(l-1))
# eviction rate for ring is a (allowed to approach 2z)
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
