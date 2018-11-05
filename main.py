import os
import argparse
import random as rand
from oram import Node
from oram import Oram
import math

def level(i):
    return math.floor(math.log(i+1,2))

def access_n(oram,n):
    for i in range(n):
        if (i%1000==0):
            print("accessing ", i)
        oram.access(i%oram.n)
    oram.print_occupancies()

# levels are 0,..l
# total number of buckets in tree is 2**(l+1)-1
# distinct real blocks are 0,...,a*(2**(l-1))
# eviction rate is a (allowed to approach 2z)

def main(l,a,s,z):
    oram = Oram(l=l, a=a, s=s, z=z)
    oram.init_pos_map()
    oram.init_tree()
    for i in range(2**oram.l):
        oram.evict()
    access_n(oram,oram.n*100)

    return oram
