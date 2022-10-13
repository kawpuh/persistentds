from functools import reduce
import vec

x = vec.BitTrie().push(3).push(4).push(5).push(6).push(6).push(7)

print(x)
print(x.push(8))
print(x)
print(reduce(lambda trie, i: trie.push(i), range(10), vec.BitTrie()))
