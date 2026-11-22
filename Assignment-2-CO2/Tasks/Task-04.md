# Assignment 2 – CO2 | Task 04

## Task 4 – Minimax growth
For branching factor b and lookahead depth d, total nodes N=1+b+...+b^d=(b^(d+1)-1)/(b-1), and leaf evaluations are b^d. The evaluation function scores board advantage at cutoff leaves (a real game can combine material, mobility, safety and objective progress). The code includes a depth-limited minimax routine and a student-defined leaf evaluation function combining material, mobility, objective progress and danger; the demonstration records evaluation calls. The script records (b,d) = (2,3), (3,4), (4,5) in results/experiments.json. Plain minimax becomes impractical when measured nodes exceed the response-time budget. A 100 ms limit is an illustrative engineering target; profile evaluation throughput on deployment hardware before choosing a maximum depth. As a separate move-quality check, an exact minimax policy for a take-1-or-2-stones game won 20 of 20 games from 10 stones against a uniform random legal opponent (100%); this is a toy validation, not evidence of strength in a commercial board game.

## Source files and evidence
- Implementation: [assignment2.py](../assignment2.py)
- Experiment outputs: [results](../results/)
- Original brief: Unit 2.docx (Tasks 1–6 and Day-4 Task 7)
