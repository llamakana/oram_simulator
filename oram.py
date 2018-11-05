
import random as rand

class Node:
    def __init__(self):
        self.real_blocks = set()
        self.counter = 0

class Oram:
    def __init__(self, l, a, s, z):
        self.pos_map = {}
        self.tree = []
        self.n = a*(2**(l-1))
        self.stash = set(range(self.n))
        self.l = l
        self.a = a
        self.s = s
        self.z = z
        self.round = 0
        self.g = 1

    def init_pos_map(self):
        for i in range(self.n):
            self.pos_map[i] = rand.randrange((2**self.l) - 1, 2**(self.l+1)-1)

    def init_tree(self):
        self.tree = [None] * (2**(self.l+1)-1)
        for i in range((2**(self.l+1)-1)):
            self.tree[i] = Node()

    def get_path(self, leaf):
        i = leaf
        path = [leaf]
        while i > 0:
            if i%2 == 0:
                i = (i-2)//2
            else:
                i = (i-1)//2
            path = path + [i]
        return path

    def evict(self):
        # leaf = 2**self.l + (self.g - 1)
        # path = self.get_path(leaf)
        # print("evicting from ", leaf)
        # self.g += 1
        # self.g = self.g % (2**self.l)

        #randomized evict for now
        leaf = rand.randrange((2**self.l) - 1, 2**(self.l+1)-1)
        path = self.get_path(leaf)
        # Read path into stash
        for x in path:

            self.stash = self.stash.union(self.tree[x].real_blocks)
            self.tree[x].real_blocks = set()
            # print(len(self.stash))
        path_len = self.l+1
        i = 0
        while i < path_len:
            current_bucket = path[i]
            self.tree[current_bucket].counter = 0

            add_to_bucket = []
            stash_paths = {}
            for b in self.stash:
                stash_paths[b] = self.get_path(self.pos_map[b])

            for a,p in stash_paths.items():
                if p[i] == current_bucket:
                    add_to_bucket.append(a)

            available_space = self.z - len(self.tree[current_bucket].real_blocks)
            # print(self.tree[current_bucket].real_blocks, available_space)
            j = len(add_to_bucket) - 1
            while available_space > 0:
                if j >= 0:
                    # print("adding ", add_to_bucket[j], " to bucket ", path[i])
                    self.tree[current_bucket].real_blocks.add(add_to_bucket[j])
                    # self.stash.remove(add_to_bucket[j])

                    # del stash_paths[add_to_bucket[j]]
                    j -= 1
                available_space -= 1
            self.stash.difference_update(self.tree[current_bucket].real_blocks)
            # print("new len", len(stash_paths))
            i += 1

        return

    def early_reshuffle(self, leaf):
        path = self.get_path(leaf)
        i = 0
        path_len = self.l + 1
        while i < path_len:
            current_bucket = path[i]
            stash_paths = {}
            add_to_bucket = []
            if self.tree[current_bucket].counter > self.s:
                self.stash = self.stash.union(self.tree[current_bucket].real_blocks)

                self.tree[current_bucket].real_blocks = set()
                self.tree[current_bucket].counter = 0

                for b in self.stash:
                    stash_paths[b] = self.get_path(self.pos_map[b])

                for a,p in stash_paths.items():
                    if p[i] == current_bucket:
                        add_to_bucket.append(a)
                j = 0
                while j < self.z:
                    if add_to_bucket:
                        self.tree[current_bucket].real_blocks.add(add_to_bucket[0])
                        add_to_bucket = add_to_bucket[1:]
                    j += 1
                self.stash.difference_update(self.tree[current_bucket].real_blocks)
            i += 1
        return


    def access(self, idx):
        leaf = self.pos_map[idx]
        current_path = self.get_path(leaf)
        # re-associate idx with new leaf
        self.pos_map[idx] = rand.randrange(2**self.l-1, 2**(self.l+1)-1)

        # remove idx from wherever it's stored in the tree if it's there
        for x in current_path:
            self.tree[x].counter += 1
            if idx in self.tree[x].real_blocks:
                self.tree[x].real_blocks.remove(idx)
        # add idx to stash
        self.stash.add(idx)
        # check if we need to evict
        self.round += 1
        if self.round == self.a:
            self.round=0
            self.evict()

        self.early_reshuffle(leaf)

        return

    def print_occupancies(self):
        for i in range(len(self.tree)):
            print(i, self.tree[i].real_blocks)
        print("Stash", self.stash)
