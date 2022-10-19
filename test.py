from functools import reduce
import vec

def debug_test_conj():
    print("[3]:", vec.PersistentBitTrie().conj(3))
    print()
    print("Empty Trie:", vec.PersistentBitTrie())
    print()
    print("[3,4]:", vec.PersistentBitTrie().conj(3).conj(4))
    print()
    print("[1..30]", reduce(lambda trie, i: trie.conj(i), range(100), vec.PersistentBitTrie()))
    print()


def debug_test_nth():
    x = reduce(lambda trie, i: trie.conj(i), range(100), vec.PersistentBitTrie())
    print("1..99")
    [print(x.nth(i)) for i in range(100)]
    pass

def debug_test_disj():
    print("[]:", vec.PersistentBitTrie().conj(3).disj())
    print()
    print("[3,4]:", vec.PersistentBitTrie().conj(3).conj(4).conj(5).disj())
    print()
    print("[1..95]", reduce(lambda trie, i: trie.conj(i), range(101), vec.PersistentBitTrie()).disj().disj().disj().disj().disj())
    print()
    print("[1..16]", reduce(lambda trie, i: trie.conj(i), range(17), vec.PersistentBitTrie()).disj())
    print()

def main():
    debug_test_disj()


main()
