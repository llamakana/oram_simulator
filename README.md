How to run:

`python -i main.py`

The `main(l,a,s,z)` function currently takes as input
  `l = number of levels in tree`
  `a = eviction rate` (this should be \leq 2Z)
  `s = early reshuffle rate`
  `z = bucket size`

Ex:
  `oram = main(8, 5, 3, 3)`

This will initialize the oram to a ring oram with distinct `n=a*2^(l-1)` real buckets.

You can inspect the buckets (stash is bucket 0) and position map with `oram.buckets`,`oram.pos_map`

For ring oram, you can also inspect the counts with `oram.counts`

Priority TODO:

  ORAM class with subclasses: Infinity (Ring)
  Vary bucket size across levels    
  Memory profiling / optimizing

Soon TODO:
  
  Switch from using python -i to getting command line arguments?
  
