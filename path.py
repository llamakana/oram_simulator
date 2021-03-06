import random as rand
from oram import Oram

class Path(Oram):
    def __init__(self, l, z, n):
        super().__init__(l, z, n)

    def access(self, idx):
        leaf = self.pos_map[idx]
        current_path = self.get_path(leaf)
        self.pos_map[idx] = rand.randrange(2**self.l, 2**(self.l+1))

        self.buckets[0].add(idx)
        # read path into stash
        for x in current_path:
            self.buckets[0].update(self.buckets[x])
            self.buckets[x] = []

        self.evict(current_path)

        return


    def evict(self, current_path):
        i = 0
        while i <= self.l:
            current_bucket = current_path[i]

            add_to_bucket = []
            # print(add_to_bucket)
            stash_paths = {}
            for b in self.buckets[0]:
                stash_paths[b] = self.get_path(self.pos_map[b])
            for a,p in stash_paths.items():
                if p[i] == current_bucket:
                    add_to_bucket.append(a)
            available_space = self.z - len(self.buckets[current_bucket])
            # print(self.tree[current_bucket].real_blocks, available_space)
            j = len(add_to_bucket) - 1
            while available_space > 0:
                if j >= 0:
                    self.buckets[current_bucket].append(add_to_bucket[j])
                    j -= 1
                available_space -= 1
            self.buckets[0].difference_update(self.buckets[current_bucket])
            # print("new len", len(stash_paths))
            i += 1
        return

class PaInf(Path):
    def __init__(self, l, z, n):
        super().__init__(l, z, n)
        self.z = -1


    def evict(self, current_path):
        i = 0
        while i <= self.l:
            current_bucket = current_path[i]

            add_to_bucket = []
            stash_paths = {}
            for b in self.buckets[0]:
                stash_paths[b] = self.get_path(self.pos_map[b])

            for a,p in stash_paths.items():
                if p[i] == current_bucket:
                    add_to_bucket.append(a)

            self.buckets[current_bucket] = add_to_bucket
            self.buckets[0].difference_update(add_to_bucket)
            # print("new len", len(stash_paths))
            i += 1

        return


    def max_rooted_subtree_size_and_depth(self, z):
        total_size = 0
        max_depth = 0
        not_empty = True
        current_level = -1
        nodes_in_level = 1
        idx = 0
        while not_empty:
            current_level += 1
            nodes_in_level = 2**current_level
            old_size = total_size
            for i in range(nodes_in_level):
                idx += 1
                if (idx == len(self.buckets)):
                    return (total_size, max_depth)
                if len(self.buckets[idx])==z:
                    total_size += 1
                    max_depth = current_level
                if i==(nodes_in_level-1):
                    if total_size == old_size:
                        return (total_size, max_depth)

        return (-1,-1)
