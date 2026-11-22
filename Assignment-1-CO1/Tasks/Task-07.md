# Assignment 1 – CO1 | Task 07

## Task 7 – Solve recurrence
Substitution gives T(l)=b^lT(0)+c(1+b+...+b^(l-1))=Θ(b^l) for b>1. Iterative deepening repeats DLS for limits 0..d; total Σ O(b^i)=O(b^d), with repeated upper levels dominated by the deepest layer.

## Source files and evidence
- Implementation: [assignment1.py](../assignment1.py)
- Experiment outputs: [results](../results/)
- Original brief: Unit 1.docx (Tasks 1–11 and Day-4 Task 12)
