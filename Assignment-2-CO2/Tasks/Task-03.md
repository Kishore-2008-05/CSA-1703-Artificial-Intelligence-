# Assignment 2 – CO2 | Task 03

## Task 3 – Alpha-beta pruning
Three binary trees model favorable order, unfavorable order and equal leaf values. Prediction: favorable order causes earlier cutoffs; unfavorable order delays or prevents them; equal leaves depend on tie handling.

| Tree | Minimax nodes | Alpha-beta nodes | Cutoffs |
|---|---:|---:|---:|
| Favorable order | 7 | 6 | 1 |
| Unfavorable order | 7 | 7 | 0 |
| Equal leaves | 7 | 6 | 1 |

The small trees make counts auditable. Branching factor/depth alone do not determine pruning performance; move ordering matters.

## Source files and evidence
- Implementation: [assignment2.py](../assignment2.py)
- Experiment outputs: [results](../results/)
- Original brief: Unit 2.docx (Tasks 1–6 and Day-4 Task 7)
