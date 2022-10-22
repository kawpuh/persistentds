import graphviz
from functools import reduce
import vec


def debug_test_conj():
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
    x = reduce(lambda trie, i: trie.conj(i), range(100),
               vec.PersistentBitTrie())
    print("1..99")
    [print(x.nth(i)) for i in range(100)]
    pass


def debug_test_disj():
    print("[]:", vec.PersistentBitTrie().conj(3).disj())
    print()
    print("[3,4]:", vec.PersistentBitTrie().conj(3).conj(4).conj(5).disj())
    print()
    print(
        "[1..95]",
        reduce(lambda trie, i: trie.conj(i), range(101),
               vec.PersistentBitTrie()).disj().disj().disj().disj().disj())
    print()
    print(
        "[1..16]",
        reduce(lambda trie, i: trie.conj(i), range(17),
               vec.PersistentBitTrie()).disj())
    print()

def viz_graph(nodes, edges):
    g = graphviz.Digraph(node_attr={"shape": "record"},
                         engine="osage")
    for node in nodes:
        g.node(*node)
    for edge in set(edges):
        g.edge(*edge)
    g.view()

def debug_test_graphviz():
    nodes, edges = [], []
    vi = vec.PersistentBitTrie()
    vs = [vi]
    for i in range(17):
        vi = vi.conj(i)
        vi.add_to_graph(nodes, edges)
        vs.append(vi)
    viz_graph(nodes, edges)
    print(vs)



def main():
    debug_test_graphviz()


main()
