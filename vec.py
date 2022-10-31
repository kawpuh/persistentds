import math

# debug_print = print
debug_print = lambda _: 0


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

    def get(self, i, default=None):
        if i >= len(self.children):
            return default
        return self.children[i]

    def walk_graph(self, nodes, edges, value_type):
        if self.leaf:
            if value_type:
                nodes.append(((
                    str(id(self)),
                    "|{ " + str(id(self)) + "|{ " +
                    "|".join(f"<f{i}> {i}"
                             for i in range(self.n)) + "}|" + "{" +
                    "|".join(str(self.get(i, '?'))
                             for i in range(self.n)) + "}" + "}|",
                ), {
                    "style": "filled"
                }))
                return
            else:
                nodes.append(((
                    str(id(self)),
                    "|{ " + str(id(self)) + "|{ " +
                    "|".join(f"<f{i}> {i}"
                             for i in range(self.n)) + "}|" + "}|",
                ), {
                    "style": "filled"
                }))
        else:
            nodes.append(
                ((str(id(self)), "|{ " + str(id(self)) + "|{ " +
                  "|".join(f"<f{i}> {i}"
                           for i in range(self.n)) + "}|" + "}|"), {}))
        for i, child in enumerate(self.children):
            edges.append((f"{id(self)}:f{i}", str(id(child))))
            if self.leaf:
                nodes.append(((str(id(child)), str(child)), {}))
            else:
                child.walk_graph(nodes, edges, value_type)

    def is_full(self):
        return len(self.children) == self.n

    def append(self, val):
        "Inserts val into first empty slot, fails if node is full"
        if len(self.children) >= self.n:
            print(f"append into a full node: {val}")
            assert 0
        self.children.append(val)

    def peek(self):
        return self.children[-1]

    def pop(self):
        return self.children.pop()

    def copy(self):
        ret = Node(self.n)
        ret.leaf = self.leaf
        ret.children = self.children.copy()
        return ret


class PersistentBitTrie:

    def __init__(self, bits=3):
        assert bits > 1
        self.size = 0
        self.bits = bits
        self.mask = (1 << self.bits) - 1
        self.root = None

    def __repr__(self):
        if self.root is None:
            return "LeafNode[]"
        return str(self.root)

    def add_to_graph(self, nodes, edges, value_type=True):
        if self.root is not None:
            self.root.walk_graph(nodes, edges, value_type)
            edges.append((str(self), str(id(self.root))))
            return nodes, edges
            # print(f"nodes: {nodes}\n\nedges:{edges}\n\n")

    def conj(self, val):
        ret = PersistentBitTrie(self.bits)
        ret.size = self.size + 1

        # overflow root?
        if self.size == 0 or math.log(
                self.size, 2**self.bits).is_integer() and self.size != 1:
            debug_print(f"conj: growing from root on {val}")
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
        depth = int(math.log(self.size, 2**self.bits))  # depth
        key = self.size
        ret.root = self.root.copy()
        walkret = ret.root
        walkself = self.root
        for key_shift in range(depth * self.bits, 0, -self.bits):
            child_idx = (key >> key_shift) & self.mask
            # print(f"key: {key}, key_shift: {key_shift}")
            # print(f"idx: {child_idx}, len: {len(walkself)}")
            if child_idx >= len(walkself):
                # create nodes the rest of the way down
                debug_print(f"conj: growing from child on {val}")
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
        depth = int(math.log(self.size, 2**self.bits))  # depth
        for key_shift in range(depth * self.bits, -self.bits, -self.bits):
            node = node[(key >> key_shift) & self.mask]
        return node

    def update(self, key, val):
        ret = PersistentBitTrie(self.bits)
        ret.size = self.size
        if val >= ret.size:
            print(f"val >= ret.size\n{val} >= {ret.size}")
            raise IndexError
        walk_self = self.root
        walk_ret = walk_self.copy()
        ret.root = walk_ret

        depth = int(math.log(self.size, 2**self.bits))  # depth
        for key_shift in range(depth * self.bits, -self.bits, -self.bits):
            lvl_key = (key >> key_shift) & self.mask
            walk_self = walk_self[lvl_key]
            if key_shift == 0:
                walk_ret[lvl_key] = val
            else:
                walk_ret[lvl_key] = walk_self.copy()
                walk_ret = walk_ret[lvl_key]
        return ret

    def pop(self):
        ret = PersistentBitTrie(self.bits)
        ret.size = self.size - 1

        # overflow root?
        if ret.size == 0 or math.log(ret.size, 2**
                                     self.bits).is_integer() and ret.size != 1:
            debug_print(f"pop: truncating from root")
            # remove node at root, promote left child
            if ret.size == 0:
                ret.root = None
            else:
                ret.root = self.root[0].copy()
            return ret

        # take the path down to our key, copying nodes along the way
        rem_key = ret.size
        key = ret.size - 1
        depth = int(math.log(
            key, 2**self.bits))  # depth, should be same for both keys
        ret.root = self.root.copy()
        walk_ret = ret.root
        walk_self = self.root
        removed = False
        for key_shift in range(depth * self.bits, 0, -self.bits):
            child_idx = (key >> key_shift) & self.mask
            rem_child_idx = (rem_key >> key_shift) & self.mask
            if child_idx != rem_child_idx:
                # Truncate path, creating nodes for remaining path
                debug_print(f"pop: truncating from child")
                walk_ret.pop()
                for _ in range(key_shift - self.bits, 0, -self.bits):
                    walk_ret[child_idx] = walk_self[child_idx].copy()
                    walk_ret, walk_self = walk_ret[child_idx], walk_self[
                        child_idx]
                removed = True
                break
            else:
                # copy node and continue
                walk_ret[child_idx] = walk_self[child_idx].copy()
                walk_ret, walk_self = walk_ret[child_idx], walk_self[child_idx]
        # we should know the idx, but easier to just append
        if not removed:
            walk_ret.pop()
        return ret

    def peek(self):
        pass


def main():
    pass


if __name__ == "__main__":
    main()
