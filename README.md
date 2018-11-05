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

You can inspect the oram stash, position map, and tree with
`oram.stash`
`oram.pos_map`
`oram.tree`

Priority TODO:
ORAM class with subclasses: Ring, Path, Infinity
Reverse Lexicographic Eviction Order
Convert tree to NumPy array
Change tree so stash is at 0 (will make indexing easier later), change functions appropriately
Record stash size after accesses

Soon TODO:
Vary bucket size across levels
