# Assignment 1 – CO1 | Task 09

## Task 9 – Performance evidence
Run python assignment1.py. Raw data: results/scaling.csv, results/test_cases.json, results/belief_states.json. Graphs: results/nodes_expanded.svg and results/runtime.svg. BFS/UCS times average five runs.

| States | BFS expanded | UCS expanded | BFS generated | UCS generated |
|---:|---:|---:|---:|---:|
| 1,000 | 978 | 979 | 993 | 1,070 |
| 10,000 | 9,961 | 9,993 | 9,981 | 10,888 |
| 100,000 | 99,985 | 99,953 | 99,996 | 108,303 |
| 1,000,000 | 999,983 | 999,957 | 999,995 | 1,085,273 |

On this synthetic sparse graph, both traverse almost all vertices. At one million states, UCS path cost was about 119,435.51 versus BFS 132,052.39, showing minimum-hop and minimum-time are different objectives.

## Source files and evidence
- Implementation: [assignment1.py](../assignment1.py)
- Experiment outputs: [results](../results/)
- Original brief: Unit 1.docx (Tasks 1–11 and Day-4 Task 12)
