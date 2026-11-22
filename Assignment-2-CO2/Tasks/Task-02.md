# Assignment 2 – CO2 | Task 02

## Task 2 – Online search agent
The rover uses online depth-first exploration: sense adjacent cells, explore an unvisited neighbour, and backtrack at dead ends. It cannot know a globally shortest route before mapping. The program compares travel moves with an offline BFS oracle on the same generated map; competitive ratio = online moves / full-map shortest path when reachable. The sample 8×8 seeds 0–2 were reachable in 14 moves with offline optimum 14 (ratio 1.0); seed 7 is an unreachable case. A further 54-run matrix varies map sizes (6, 8, 12), target distance (middle and far corner), obstacle/dead-end density (0.05, 0.16, 0.30) and seeds 11–13; raw moves, revisits, reachability and competitive ratios are in results/online_dfs_experiments.csv. On the 12×12 middle-target cases at density 0.16, successful runs had ratios about 5.83–8.00; at density 0.30 some targets were unreachable. This supports the conclusion that larger maps, detours and dead ends can make online exploration expensive. These are synthetic demonstrations, not statistical guarantees.

Online DFS is reasonable for one-off exploration and small/unknown facilities. It is less suitable for repeated missions in stable maps because exploration cost is paid again. For 20 rovers in 20 facilities with maps unchanged for months, perform an initial mapping survey, share validated maps, then use offline A*/Dijkstra; retain online exploration for unexpected closures.

## Source files and evidence
- Implementation: [assignment2.py](../assignment2.py)
- Experiment outputs: [results](../results/)
- Original brief: Unit 2.docx (Tasks 1–6 and Day-4 Task 7)
