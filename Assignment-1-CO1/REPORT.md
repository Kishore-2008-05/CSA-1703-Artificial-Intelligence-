# Assignment 1 – CO1: Hospital Medicine-Delivery Robot

**CSA17 Artificial Intelligence · Python 3 · Tasks 1–12**

## Summary
This project compares BFS, UCS and recursive depth-limited DFS on a weighted hospital graph. BFS minimizes edge count, not travel time. UCS is the recommended production planner because it finds a minimum-cost route when edge costs are non-negative. DLS is a low-memory bounded search but is not complete beyond its depth limit and is not cost-optimal.

## Task 1 – Agent and problem formulation
**PEAS:** Performance—correct medicine/ward, safe route, low travel time and battery use; Environment—pharmacy, corridors, junctions, lifts, ward doors, people and closures; Actuators—motors, lift/door interface and delivery compartment; Sensors—odometry, camera/LiDAR, localization and obstacle/lift status.

The graph abstraction is partially observable in practice, mostly deterministic in the static route model, sequential, dynamic, discrete (physical motion is continuous), and multi-agent because people and other robots share corridors. The rational-agent view is **acting rationally**: choose actions that maximize expected delivery performance. This is a goal-based problem-solving agent in the symbolic state/operator/goal/cost tradition of early AI.

State = graph vertex; initial state = pharmacy; actions = traverse connected edge; transition = move to adjacent vertex; goal test = requested ward; path cost = sum of non-negative travel-time weights.

**BFS:** queue; remove front; test goal; enqueue undiscovered neighbours and record parents. **UCS:** min-heap of (cost,state); remove cheapest current entry; test goal; relax outgoing edges and push improved costs. **Recursive DLS:** test goal and depth limit; recursively visit unvisited neighbours; return on success, otherwise backtrack. BFS is a minimum-hop baseline, UCS is appropriate for weighted routes, and DLS studies bounded recursive memory. Preprocessing builds adjacency lists and validates costs: O(V+E).

## Task 2 – Basic operation
BFS: successor inspection/discovery/enqueue; each vertex is expanded once. UCS: edge relaxation and heap insertion/removal; heap operations add a logarithmic factor. DLS: recursive node expansion and successor inspection. These counts represent actual search work more reliably than elapsed time alone.

## Task 3 – Time and space derivation
With branching factor b, shallowest goal depth d, maximum depth m, optimal cost C* and minimum positive edge cost ε, nodes through depth d are 1+b+...+b^d = (b^(d+1)-1)/(b-1) = Θ(b^d).
BFS tree-search time is Θ(b^d) and frontier/duplicate storage can be Θ(b^d); graph implementation is O(V+E). UCS with a binary heap is O((V+E)log V) time and O(V) graph-search storage; cost-bounded exploration depends on the C*/ε contour. DLS with limit l takes Θ(b^l) time and O(bl) recursion/path storage. Add adjacency construction O(V+E) to every total.

## Task 4 – Best/average/worst
BFS best: goal=start or first shallow neighbour; worst: deep/unreachable goal requiring broad exploration. UCS best: goal is cheapest first; worst: many cheaper detours must be settled first. DLS best: goal on first branch within limit; worst: goal beyond limit or unreachable, forcing exploration to depth l. Average work depends on graph shape, costs and neighbour order, not a universal constant.

## Task 5 – Asymptotic comparison
BFS graph search O(V+E); UCS binary-heap search O((V+E)log V); DLS O(b^l) time and O(bl) stack/path space. On sparse graphs, growing from 1,000 to 1,000,000 states makes graph storage and duplicate detection important. DLS reduces frontier storage but sacrifices completeness/optimality.

## Task 6 – Recurrence
For recursive DLS, remaining depth l: T(0)=c0, T(l)=bT(l-1)+c. There are b child subproblems of size l-1; c is local goal/depth/successor work.

## Task 7 – Solve recurrence
Substitution gives T(l)=b^lT(0)+c(1+b+...+b^(l-1))=Θ(b^l) for b>1. Iterative deepening repeats DLS for limits 0..d; total Σ O(b^i)=O(b^d), with repeated upper levels dominated by the deepest layer.

## Task 8 – Implementation and test
assignment1.py implements BFS, UCS, recursive DLS and seeded sparse graph generation. Cases: reachable 0→119, unreachable 0→120, start=goal 10→10; DLS is validated on a small graph to avoid Python recursion limits. BFS/UCS share seeded graph and start/goal pairs at 1k, 10k, 100k and 1m vertices.

## Task 9 – Performance evidence
Run python assignment1.py. Raw data: results/scaling.csv, results/test_cases.json, results/belief_states.json. Graphs: results/nodes_expanded.svg and results/runtime.svg. BFS/UCS times average five runs.

| States | BFS expanded | UCS expanded | BFS generated | UCS generated |
|---:|---:|---:|---:|---:|
| 1,000 | 978 | 979 | 993 | 1,070 |
| 10,000 | 9,961 | 9,993 | 9,981 | 10,888 |
| 100,000 | 99,985 | 99,953 | 99,996 | 108,303 |
| 1,000,000 | 999,983 | 999,957 | 999,995 | 1,085,273 |

On this synthetic sparse graph, both traverse almost all vertices. At one million states, UCS path cost was about 119,435.51 versus BFS 132,052.39, showing minimum-hop and minimum-time are different objectives.

## Task 10 – Theory versus experiment
Counts grow approximately linearly with V because E=O(V) and the generated graph is connected. UCS produces more heap entries and higher runtime. The corridor-like graph keeps the frontier relatively small; this is not guaranteed for high-branching maps.

## Task 11 – Recommendation
Choose UCS for weighted travel-time optimality. Use BFS only if every move has equal cost or hop count is the objective. Use DLS for bounded reachability diagnostics, not as the primary route planner. Include preprocessing and map updates in profiling.

## Task 12 – Sensor/localisation failure
The robot no longer knows one exact start vertex; its information state is a belief set of k candidate junctions. There can be up to 2^V possible belief subsets. **Decision: modify** the design: use local sensing/odometry to reduce the candidate set, then run UCS from the identified junction. Without sensing, a safe conditional policy must work from every candidate and may be much more expensive or impossible. results/belief_states.json records the subset upper bound for k=2,4,8 and a simple action proxy with/without a local sensor. This is an illustrative model, not a physical robot test.

## Reproducibility and limitations
Python 3, standard library, seed 17. Timings are machine-dependent; operation counts are primary. Synthetic sparse graph, not a hospital map. DLS is tested only at shallow depth because Python recursion limits make it unsuitable for million-deep paths. No physical robot, lift, door or localization hardware was tested.
