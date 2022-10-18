import math

# debug_print = print
debug_print = lambda _ : 0


class Empty:
    pass


class Node:

    def __init__(self, n, leaf=False):
        self.n = n
        self.leaf = leaf
        self.children = []

    def __getitem__(self, i):
        return self.children[i]

    def __setitem__(self, i, val):
        self.children[i] = val

    def __len__(self):
        return len(self.children)

    def __repr__(self):
        return f"{'Leaf' if self.leaf else ''}Node[{', '.join(repr(child) for child in self.children)}]"

    def is_full(self):
        return len(self.children) == self.n

    def append(self, val):
        "Inserts val into first empty slot, fails if node is full"
        if len(self.children) >= self.n:
            print(f"append into a full node")
            assert 0
        self.children.append(val)

    def peek(self):
        return self.children[-1]

    def copy(self):
        ret = Node(self.n)
        ret.leaf = self.leaf
        ret.children = self.children.copy()
        return ret


class PersistentBitTrie:

    def __init__(self, n=3):
        assert n > 1
        self.size = 0
        self.bits = n
        self.mask = (1 << self.bits) - 1
        self.root = None

    def __repr__(self):
        return str(self.root)

    def append(self, val):
        ret = PersistentBitTrie(self.bits)
        ret.size = self.size + 1

        # overflow root?
        if self.size == 0 or math.log(self.size, 2**self.bits).is_integer() and self.size != 1:
            debug_print(f"append: growing from root on {val}")
            # add a new node at root for space, then create a path to our leaf
            ret.root = Node(2**self.bits)
            walk = ret.root
            if self.size != 0:
                ret.root.append(self.root)
                goal_depth = math.ceil(math.log(self.size + 1, self.mask))
                for _ in range(1, goal_depth):
                    walk.append(Node(2**self.bits))
                    walk = walk.peek()
            walk.leaf = True
            walk.append(val)
            return ret

        # take the path down to our key, copying or creating nodes along the way
        depth = int(math.log(self.size, 2**self.bits)) # depth
        key = self.size
        ret.root = self.root.copy()
        walkret = ret.root
        walkself = self.root
        for key_shift in range(depth*self.bits, 0, -self.bits):
            child_idx = (key >> key_shift) & self.mask
            # print(f"key: {key}, key_shift: {key_shift}")
            # print(f"idx: {child_idx}, len: {len(walkself)}")
            if child_idx >= len(walkself):
                # create nodes the rest of the way down
                debug_print(f"append: growing from child on {val}")
                for _ in range(key_shift, 0, -self.bits):
                    walkret.append(Node(2**self.bits))
                    walkret = walkret.peek()
                walkret.leaf = True
                break
            else:
                # copy node and continue
                walkret[child_idx] = walkself[child_idx].copy()
                walkret, walkself = walkret[child_idx], walkself[child_idx]
        # we should know the idx, but easier to just append
        walkret.append(val)

        return ret

    def nth(self, key):
        node = self.root
        depth = int(math.log(self.size, 2**self.bits)) # depth
        for key_shift in range(depth*self.bits, -self.bits, -self.bits):
            node = node[(key >> key_shift) & self.mask]
        return node

def main():
    pass


if __name__ == "__main__":
    main()
