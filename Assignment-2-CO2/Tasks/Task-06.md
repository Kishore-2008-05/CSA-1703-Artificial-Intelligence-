# Assignment 2 – CO2 | Task 06

## Task 6 – Exhaustive and local search
A tour fixes depot 0 first, permutes the remaining customers and includes the return edge. Exhaustive enumeration checks (n-1)! tours and retains the minimum. The small Euclidean circle instances provide independently verifiable optima.

| Cities including depot | Candidate tours |
|---:|---:|
| 6 | 120 |
| 7 | 720 |
| 8 | 5,040 |

The local alternative is 2-opt hill climbing with random restarts. Twenty seeds are run per instance; raw costs and percentage gaps are in results/experiments.json. For these regular circle instances mean gap was 0% for each size; this does not prove 2-opt is always optimal. Other layouts can contain local minima or plateaus. Each additional customer multiplies exhaustive candidates by the previous customer count. In this prototype, use exhaustive search only for small tours (about 8–9 cities); switch to 2-opt or another bounded method for larger cases and validate route quality.

## Source files and evidence
- Implementation: [assignment2.py](../assignment2.py)
- Experiment outputs: [results](../results/)
- Original brief: Unit 2.docx (Tasks 1–6 and Day-4 Task 7)
