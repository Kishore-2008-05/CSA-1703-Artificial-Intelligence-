# Assignment 1 – CO1 | Task 03

## Task 3 – Time and space derivation
With branching factor b, shallowest goal depth d, maximum depth m, optimal cost C* and minimum positive edge cost ε, nodes through depth d are 1+b+...+b^d = (b^(d+1)-1)/(b-1) = Θ(b^d).
BFS tree-search time is Θ(b^d) and frontier/duplicate storage can be Θ(b^d); graph implementation is O(V+E). UCS with a binary heap is O((V+E)log V) time and O(V) graph-search storage; cost-bounded exploration depends on the C*/ε contour. DLS with limit l takes Θ(b^l) time and O(bl) recursion/path storage. Add adjacency construction O(V+E) to every total.

## Source files and evidence
- Implementation: [assignment1.py](../assignment1.py)
- Experiment outputs: [results](../results/)
- Original brief: Unit 1.docx (Tasks 1–11 and Day-4 Task 12)
