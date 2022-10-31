import graphviz
from functools import reduce
import vec


def debug_test_conj():
    # TODO: write asserts
    print("[3]:", vec.PersistentBitTrie().conj(3))
    print()
    print("Empty Trie:", vec.PersistentBitTrie())
    print()
    print("[3,4]:", vec.PersistentBitTrie().conj(3).conj(4))
    print()
    print(
        "[1..30]",
        reduce(lambda trie, i: trie.conj(i), range(100),
               vec.PersistentBitTrie()))
    print()


def debug_test_nth():
    # TODO: write asserts
    x = reduce(lambda trie, i: trie.conj(i), range(100),
               vec.PersistentBitTrie())
    print("1..99")
    [print(x.nth(i)) for i in range(100)]
    pass


def debug_test_pop():
    print("[]")
    assert str(vec.PersistentBitTrie().conj(3).pop()) == "LeafNode[]"
    print()
    print("[3,4]")
    assert str(vec.PersistentBitTrie().conj(3).conj(4).conj(
        5).pop()) == "LeafNode[3, 4]"
    print()
    # TODO: write asserts
    print(
        "[0..95]",
        reduce(lambda trie, i: trie.conj(i), range(101),
               vec.PersistentBitTrie()).pop().pop().pop().pop().pop())
    print()
    print(
        "[0..15]",
        reduce(lambda trie, i: trie.conj(i), range(17),
               vec.PersistentBitTrie()).pop())
    print()


def viz_graph(nodes, edges):
    g = graphviz.Digraph(node_attr={"shape": "record"},
                         graph_attr={
                             "rankdir": "LR",
                             "ordering": "in",
                         },
                         filename="graph.gv",
                         format="webp")
    for node_args, node_kwargs in nodes:
        g.node(*node_args, **node_kwargs)
    for edge in set(edges):
        g.edge(*edge)
    g.view()


def debug_test_graphviz():
    nodes, edges = [], []
    vi = vec.PersistentBitTrie(bits=2)
    vs = [vi]
    for i in range(17):
        vi = vi.conj(i)
        vi.add_to_graph(nodes, edges, True)
        vs.append(vi)
    viz_graph(nodes, edges)
    print(vs)


def debug_test_nth():
    x = reduce(lambda trie, i: trie.conj(i), range(101),
               vec.PersistentBitTrie()).pop().pop().pop().pop().pop()
    print("Testing nth for [0..95] vec")
    # "[0..95]",
    for i in range(95):
        if not x.nth(i) == i:
            print(f"{x.nth(i)} and {i+1}")
            return
    print("Success")


def debug_test_update():
    x = reduce(lambda trie, i: trie.conj(i), range(101),
               vec.PersistentBitTrie()).pop().pop().pop().pop().pop()
    print("Updating [0..95] vec @ 55 to 80")
    assert x.nth(55) == 55
    y = x.update(55, 80)
    if not y.nth(55) == 80:
        print(f"{y.nth(55)} and {80}")
        return
    print("Success")

    print("Flipping [0..95]")
    z = x.update(0, 0)
    for i, val in enumerate(range(95, -1, -1)):
        z = z.update(i, val)
    for i, val in enumerate(range(95, -1, -1)):
        assert z.nth(i) == val
    print(z)


def debug_test_suite():
    debug_test_conj()
    debug_test_nth()
    debug_test_pop()
    debug_test_nth()
    debug_test_update()


def main():
    debug_test_graphviz()


main()
