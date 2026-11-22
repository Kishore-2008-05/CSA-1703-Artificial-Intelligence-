# Assignment 2 – CO2 | Task 07

## Task 7 – Diagnose, redesign and validate
**Bottleneck:** alpha-beta pruning is sensitive to child ordering; in the poor-order fixture no cutoff occurred. **Objective:** reduce visited nodes without changing minimax value.

**Redesign:** rank candidate moves with a cheap static estimate, then explore likely-best children first so alpha/beta bounds tighten earlier.

Prediction: better order reduces expanded nodes and increases cutoffs, at the cost of scoring/sorting overhead. In the sample, baseline alpha-beta visited 18 nodes and had 2 cutoffs; ordered prototype visited 15 nodes and had 3 cutoffs (16.7% fewer nodes). Both returned value 5. The gain is modest; expensive exact ordering would not be justified. A practical engine should use inexpensive estimates and measure total runtime as well as node count.

## Source files and evidence
- Implementation: [assignment2.py](../assignment2.py)
- Experiment outputs: [results](../results/)
- Original brief: Unit 2.docx (Tasks 1–6 and Day-4 Task 7)
