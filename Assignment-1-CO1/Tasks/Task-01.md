# Assignment 1 – CO1 | Task 01

## Task 1 – Agent and problem formulation
**PEAS:** Performance—correct medicine/ward, safe route, low travel time and battery use; Environment—pharmacy, corridors, junctions, lifts, ward doors, people and closures; Actuators—motors, lift/door interface and delivery compartment; Sensors—odometry, camera/LiDAR, localization and obstacle/lift status.

The graph abstraction is partially observable in practice, mostly deterministic in the static route model, sequential, dynamic, discrete (physical motion is continuous), and multi-agent because people and other robots share corridors. The rational-agent view is **acting rationally**: choose actions that maximize expected delivery performance. This is a goal-based problem-solving agent in the symbolic state/operator/goal/cost tradition of early AI.

State = graph vertex; initial state = pharmacy; actions = traverse connected edge; transition = move to adjacent vertex; goal test = requested ward; path cost = sum of non-negative travel-time weights.

**BFS:** queue; remove front; test goal; enqueue undiscovered neighbours and record parents. **UCS:** min-heap of (cost,state); remove cheapest current entry; test goal; relax outgoing edges and push improved costs. **Recursive DLS:** test goal and depth limit; recursively visit unvisited neighbours; return on success, otherwise backtrack. BFS is a minimum-hop baseline, UCS is appropriate for weighted routes, and DLS studies bounded recursive memory. Preprocessing builds adjacency lists and validates costs: O(V+E).

## Source files and evidence
- Implementation: [assignment1.py](../assignment1.py)
- Experiment outputs: [results](../results/)
- Original brief: Unit 1.docx (Tasks 1–11 and Day-4 Task 12)
