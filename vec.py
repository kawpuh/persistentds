import math


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
            print("pushing into a full node")
            assert 0
        self.children.append(val)

    def peek(self):
        return self.children[-1]
    # def peek(self):
    #     "Return val in last non-empty slot or Empty otherwise"
    #     ret = Empty
    #     for child in self.children:
    #         if child is Empty:
    #             return ret
    #         ret = child
    #     return ret

    def copy(self):
        ret = Node(self.n)
        ret.leaf = self.leaf
        ret.children = self.children.copy()
        return ret


class BitTrie:

    def __init__(self, n=5):
        self.size = 0
        self.n = n
        self.mask = (1 << self.n) - 1
        self.root = None

    def __repr__(self):
        return str(self.root)

    def push(self, val):
        ret = BitTrie(self.n)
        ret.size = self.size + 1
        if self.root is None:
            ret.root = Node(self.n)
            ret.root.append(val)
            ret.root.leaf = True
            return ret
        walk_src = self.root

        # check if we're full
        # print(f"n: {self.n} size: {self.size} res: {math.log(self.size, self.n)}")
        if math.log(self.size, self.n).is_integer() and self.n != 1 and self.size != 1:
            # add a new node at root for space, then create a path to our leaf
            print(f"here {val}")
            ret.root = Node(self.n)
            ret.root.append(self.root)

            walk = ret.root
            depth = 1
            goal_depth = math.ceil(math.log(self.size + 1, self.n))
            for _ in range(depth, goal_depth):
                walk.append(Node(self.n))
                walk = walk.peek()
            walk.leaf = True
            walk.append(val)
            return ret

        walk_end = self.root
        while not walk_end.leaf:
            walk_end = walk_end.peek()

        walk_src = self.root
        walk_dest = walk_src.copy()
        ret.root = walk_dest
        # See if we'll have room in a leaf
        if not walk_end.is_full():
            # TODO: copy path and insert
            while not walk_dest.leaf:
                walk_dest[-1] = walk_src.peek().copy()
                walk_dest, walk_src = walk_dest.peek(), walk_src.peek()
            walk_dest.append(val)
            return ret
        else:
            # We'll have to branch and create a new path before the leaf
            depth = 0
            goal_depth = math.ceil(math.log(self.size + 1, self.n))
            while walk_dest.is_full():
                depth += 1
                walk_dest[-1] = walk_src.peek().copy()
                walk_dest, walk_src = walk_dest.peek(), walk_src.peek()
            for _ in range(depth, goal_depth):
                walk_dest.append(Node(self.n))
                walk_dest = walk_dest.peek()
            walk_dest.leaf = True
            walk_dest.append(val)
            return ret

    # def lookup(self, key):
    #     # FIXME: untested code copied from pseudocode
    #     node = self.root
    #     for level in range(self.shift, 0, -self.branching):
    #         node = node[(key >> level) & self.mask]
    #     return node

    # def __str__(self):
    #     arr = []
    #     stack = [self.root]
    #     while len(stack) > 0:
    #         walk = stack.pop()
    #         if walk.


def main():
    pass


if __name__ == "__main__":
    main()
