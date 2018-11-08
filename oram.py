
import random as rand

class Oram:
    def __init__(self, l, z):
        self.l = l
        self.n = 2**l
        self.z = z
        self.pos_map = []
        self.buckets = []

    def init_pos_map(self):
        self.pos_map = [0] * (self.n+1)
        for i in range(1, self.n+1):
            self.pos_map[i] = rand.randint(2**self.l, 2**(self.l+1)-1)

    def init_tree(self):
        self.buckets = [[]] * (2**(self.l+1))
        self.buckets[0] = set(range(1,self.n+1))

    def print_occupancies(self):
        for i in range(len(self.buckets)):
            print("Bucket", i, self.buckets[i])

    def get_path(self, leaf):
        i = leaf
        path = [leaf]
        while i > 1:
            if i%2 == 0:
                i = i//2
            else:
                i = (i-1)//2
            path = path + [i]
        return path

class Path(Oram):
    def __init__(self, l, z):
        super().__init__(l, z)

    def evict(self):
        return

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
            del stash_paths
            del add_to_bucket
            i += 1

        return

class Ring(Oram):
    def __init__(self, l, a, s, z):
        super().__init__(l, z)
        self.counters = [0] * (2**(l+1))
        self.a = a
        self.s = s
        self.n = a*(2**(l-1))
        self.round = 0
        self.g = 0

    def evict(self):
        # leaf = 2**self.l + self.g
        # path = self.get_path(leaf)
        # print("evicting from ", leaf)
        # self.g += 1
        # self.g = self.g % (2**self.l)

        #randomized evict for now
        leaf = rand.randint(2**self.l, 2**(self.l+1)-1)
        path = self.get_path(leaf)

        # Read path into stash
        for x in path:
            self.buckets[0] = self.buckets[0].union(self.buckets[x])
            self.buckets[x] = []
            # print(len(self.buckets[0]))
        i = 0
        while i <= self.l:
            current_bucket = path[i]
            self.counters[current_bucket] = 0

            add_to_bucket = []
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
                    # print("adding ", add_to_bucket[j], " to bucket ", path[i])
                    self.buckets[current_bucket].append(add_to_bucket[j])
                    # self.buckets[0].remove(add_to_bucket[j])

                    # del stash_paths[add_to_bucket[j]]
                    j -= 1
                available_space -= 1
            self.buckets[0].difference_update(self.buckets[current_bucket])
            # print("new len", len(stash_paths))
            del stash_paths
            del add_to_bucket
            i += 1

        return

    def early_reshuffle(self, leaf):
        path = self.get_path(leaf)
        i = 0
        while i <= self.l:
            current_bucket = path[i]
            stash_paths = {}
            add_to_bucket = []
            if self.counters[current_bucket] > self.s:
                self.buckets[0].update(self.buckets[current_bucket])
                self.buckets[current_bucket] = []
                self.counters[current_bucket] = 0

                for b in self.buckets[0]:
                    stash_paths[b] = self.get_path(self.pos_map[b])

                for a,p in stash_paths.items():
                    if p[i] == current_bucket:
                        add_to_bucket.append(a)
                j = 0
                while j < self.z:
                    if add_to_bucket:
                        self.buckets[current_bucket].append(add_to_bucket[0])
                        add_to_bucket = add_to_bucket[1:]
                    j += 1
                self.buckets[0].difference_update(self.buckets[current_bucket])
            del stash_paths
            del add_to_bucket
            i += 1

        return


    def access(self, idx):
        leaf = self.pos_map[idx]
        current_path = self.get_path(leaf)
        # re-associate idx with new leaf
        self.pos_map[idx] = rand.randrange(2**self.l, 2**(self.l+1))

        # remove idx from wherever it's stored in the tree if it's there
        for x in current_path:
            self.counters[x] += 1
            if idx in self.buckets[x]:
                self.buckets[x].remove(idx)
                self.buckets[0].add(idx)

        # check if we need to evict
        self.round += 1
        if self.round == self.a:
            self.round=0
            self.evict()

        self.early_reshuffle(leaf)

        return
