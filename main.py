import os
import argparse
import random as rand
# from oram import Node
from oram import Oram
from oram import Ring
import math
import sys


def access_n(oram,rounds):
    for i in range(rounds):
        print("Accessing 1 through n round ", i)
        for j in range(1,oram.n+1):
            oram.access(j)
        oram.print_occupancies()
    # for i in range(1, n+1):
    #     if (i%1000==0):
    #         print("accessing ", i)
    #     oram.access(i%oram.n)
    # oram.print_occupancies()

# levels are 0,..l
# total number of buckets in tree is 2**(l+1)-1
# distinct real blocks are 0,...,a*(2**(l-1))
# eviction rate is a (allowed to approach 2z)

def main(l,a,s,z):
    oram = Ring(l=l, a=a, s=s, z=z)
    oram.init_pos_map()
    oram.init_tree()
    print("initialized!")
    for i in range(2**oram.l):
        oram.evict()
    print("Beginning accesses")
    access_n(oram,100)

    return oram
