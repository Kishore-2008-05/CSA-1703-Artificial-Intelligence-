# Assignment 2 – CO2: Searching Techniques

**CSA17 Artificial Intelligence · Python 3 · Tasks 1–7**

## Summary
Experiments cover informed search, online exploration, minimax/alpha-beta, CSP propagation, exhaustive TSP, local search and a redesign. A* retains optimality with Manhattan distance on four-neighbour unit-cost grids; Greedy can expand fewer nodes but return a longer route. Alpha-beta depends on move ordering. Constraint propagation reduces decisions on the sample CSP. Exhaustive TSP grows factorially; 2-opt is practical but not guaranteed optimal.

## Task 1 – UCS, Greedy and A*
Grid moves are four-directional and cost one. The heuristic is Manhattan distance h(r,c)=|r-r_goal|+|c-c_goal|. It is admissible because removing obstacles creates a relaxed grid whose shortest route is exactly Manhattan distance; obstacles cannot shorten it. It is consistent because one move changes h by at most one.

**Predictions before implementation:** UCS expands by accumulated path cost and is optimal. Greedy expands nodes closest to the goal by h, often quickly on open maps but can be misled by obstacles and is not optimal. A* balances g+h and is optimal with this consistent heuristic.

Four 25×25 maps are tested: open, cluttered, maze and a wall-with-gap trap. Raw metrics are in results/grid_search.csv. On the cluttered map Greedy returned cost 52 versus optimal cost 48; UCS and A* returned 48. Other maps had cost 48 for all three. With 95% of trips on open roads, recommend A* as default: it retains optimality and uses the heuristic; Greedy is a speed-oriented option only if suboptimal routes are acceptable.

## Task 2 – Online search agent
The rover uses online depth-first exploration: sense adjacent cells, explore an unvisited neighbour, and backtrack at dead ends. It cannot know a globally shortest route before mapping. The program compares travel moves with an offline BFS oracle on the same generated map; competitive ratio = online moves / full-map shortest path when reachable. The sample 8×8 seeds 0–2 were reachable in 14 moves with offline optimum 14 (ratio 1.0); seed 7 is included as an unreachable case. These are synthetic demonstrations, not statistical guarantees.

Online DFS is reasonable for one-off exploration and small/unknown facilities. It is less suitable for repeated missions in stable maps because exploration cost is paid again. For 20 rovers in 20 facilities with maps unchanged for months, perform an initial mapping survey, share validated maps, then use offline A*/Dijkstra; retain online exploration for unexpected closures.

## Task 3 – Alpha-beta pruning
Three binary trees model favorable order, unfavorable order and equal leaf values. Prediction: favorable order causes earlier cutoffs; unfavorable order delays or prevents them; equal leaves depend on tie handling.

| Tree | Minimax nodes | Alpha-beta nodes | Cutoffs |
|---|---:|---:|---:|
| Favorable order | 7 | 6 | 1 |
| Unfavorable order | 7 | 7 | 0 |
| Equal leaves | 7 | 6 | 1 |

The small trees make counts auditable. Branching factor/depth alone do not determine pruning performance; move ordering matters.

## Task 4 – Minimax growth
For branching factor b and lookahead depth d, total nodes N=1+b+...+b^d=(b^(d+1)-1)/(b-1), and leaf evaluations are b^d. The evaluation function scores board advantage at cutoff leaves (a real game can combine material, mobility, safety and objective progress). The script records (b,d) = (2,3), (3,4), (4,5) in results/experiments.json. Plain minimax becomes impractical when measured nodes exceed the response-time budget. A 100 ms limit is an illustrative engineering target; profile evaluation throughput on deployment hardware before choosing a maximum depth.

## Task 5 – Constraint propagation
Variables are exams; domains are possible time slots. An edge (X,Y) means shared students require different slots. Revise(X,Y) removes x if no y in D(Y) satisfies x != y. After a domain shrinks, re-enqueue adjacent arcs. An empty domain means failure. Backtracking selects a smallest remaining domain and assigns a slot; propagation runs after each assignment.

Correctness: a value with no compatible neighbour value cannot appear in any valid complete assignment, so removing it cannot remove a solution. Arc consistency is not complete for all CSPs; backtracking is still needed. The four-exam cycle needed 6 decision nodes and 2 backtracks without propagation versus 1 decision and 0 backtracks with propagation (43 support checks). A contradictory unary-domain example (P={1}, Q={1}, P!=Q) creates an empty domain before search. Domain states are returned in JSON; domain cardinality can be plotted to show shrinkage.

## Task 6 – Exhaustive and local search
A tour fixes depot 0 first, permutes the remaining customers and includes the return edge. Exhaustive enumeration checks (n-1)! tours and retains the minimum. The small Euclidean circle instances provide independently verifiable optima.

| Cities including depot | Candidate tours |
|---:|---:|
| 6 | 120 |
| 7 | 720 |
| 8 | 5,040 |

The local alternative is 2-opt hill climbing with random restarts. Twenty seeds are run per instance; raw costs and percentage gaps are in results/experiments.json. For these regular circle instances mean gap was 0% for each size; this does not prove 2-opt is always optimal. Other layouts can contain local minima or plateaus. Each additional customer multiplies exhaustive candidates by the previous customer count. In this prototype, use exhaustive search only for small tours (about 8–9 cities); switch to 2-opt or another bounded method for larger cases and validate route quality.

## Task 7 – Diagnose, redesign and validate
**Bottleneck:** alpha-beta pruning is sensitive to child ordering; in the poor-order fixture no cutoff occurred. **Objective:** reduce visited nodes without changing minimax value.

**Redesign:** rank candidate moves with a cheap static estimate, then explore likely-best children first so alpha/beta bounds tighten earlier.

Prediction: better order reduces expanded nodes and increases cutoffs, at the cost of scoring/sorting overhead. In the sample, baseline alpha-beta visited 18 nodes and had 2 cutoffs; ordered prototype visited 15 nodes and had 3 cutoffs (16.7% fewer nodes). Both returned value 5. The gain is modest; expensive exact ordering would not be justified. A practical engine should use inexpensive estimates and measure total runtime as well as node count.

## Reproducibility and limitations
Run python assignment2.py from this folder. Python standard library only; fixed random seeds are in source. results/grid_search.csv and results/experiments.json contain raw metrics. Times are machine-dependent. All maps, game trees, timetables and delivery locations are synthetic teaching fixtures, not real operational data.
