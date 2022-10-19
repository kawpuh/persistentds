# Notes
## What?
- Playing around with implementing clojure's persistent data structures in python
- Most of the relevant implementation for vector is [here](https://github.com/clojure/clojure/blob/master/src/jvm/clojure/lang/PersistentVector.java)

## Ops
- update:
    1. walk from head to leaf duplicating each node
    2. make the appropriate update in duplicated leaf

- conj:
    1. walk from head to rightmost leaf. if there is space there, simply copy the path and insert
    2. if there wasn't enough space, copy path from head until last non-leaf without a right pointer.make new nodes for the path from that right pointer to a new leaf with the appended value
    3. if there's no space @ leaf and no empty right pointers then root then we have to add another level. root points to a new node with left pointer going to old list and right pointer going to a new path down to a new leaf with the appended value

- disj:
    - three cases corresponding to undoing the three cases in append

## Indexing



## Misc
- persistent bit-partitioned vector trie
- balanced ordered tree
    - balanced :: tree with invariant: height of child subtrees differ by <= 1
- and except it's a trie instead of tree
- trie :: nodes are traversed incrementally consuming the key
- with the additional constraint that values are only held in leaves


- TODO: transients and tail
