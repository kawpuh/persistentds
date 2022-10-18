from functools import reduce
import vec

def debug_test_append():
    print("[3]:", vec.PersistentBitTrie().append(3))
    print()
    print("Empty Trie:", vec.PersistentBitTrie())
    print()
    print("[3,4]:", vec.PersistentBitTrie().append(3).append(4))
    print()
    print("[1..30]", reduce(lambda trie, i: trie.append(i), range(100), vec.PersistentBitTrie()))
    print()


def debug_test_nth():
    x = reduce(lambda trie, i: trie.append(i), range(100), vec.PersistentBitTrie())
    print("1..99")
    [print(x.nth(i)) for i in range(100)]
    pass

def main():
    debug_test_append()
    debug_test_nth()


main()
