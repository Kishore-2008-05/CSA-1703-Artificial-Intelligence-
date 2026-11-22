# Assignment 2 – CO2 | Task 01

## Task 1 – UCS, Greedy and A*
Grid moves are four-directional and cost one. The heuristic is Manhattan distance h(r,c)=|r-r_goal|+|c-c_goal|. It is admissible because removing obstacles creates a relaxed grid whose shortest route is exactly Manhattan distance; obstacles cannot shorten it. It is consistent because one move changes h by at most one.

**Predictions before implementation:** UCS expands by accumulated path cost and is optimal. Greedy expands nodes closest to the goal by h, often quickly on open maps but can be misled by obstacles and is not optimal. A* balances g+h and is optimal with this consistent heuristic.

Four 25×25 maps are tested: open, cluttered, maze and a wall-with-gap trap. Raw metrics are in results/grid_search.csv and visual comparison in results/grid_expansions.svg. On the cluttered map Greedy returned cost 52 versus optimal cost 48; UCS and A* returned 48. Other maps had cost 48 for all three. With 95% of trips on open roads, recommend A* as default: it retains optimality and uses the heuristic; Greedy is a speed-oriented option only if suboptimal routes are acceptable.

## Source files and evidence
- Implementation: [assignment2.py](../assignment2.py)
- Experiment outputs: [results](../results/)
- Original brief: Unit 2.docx (Tasks 1–6 and Day-4 Task 7)
