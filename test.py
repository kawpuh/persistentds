from functools import reduce
import vec

def debug_test_conj():
    print("[3]:", vec.BitTrie().append(3))
    print()
    print("Empty Trie:", vec.BitTrie())
    print()
    print("[3,4]:", vec.BitTrie().append(3).append(4))
    print()
    print("[1..30]", reduce(lambda trie, i: trie.conj(i), range(100), vec.BitTrie()))
    print()


def debug_test_get():
    # vec.BitTrie()._lookup(3)
    pass

def main():
    debug_test_conj()


main()
