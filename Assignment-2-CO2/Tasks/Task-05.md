# Assignment 2 – CO2 | Task 05

## Task 5 – Constraint propagation
Variables are exams; domains are possible time slots. An edge (X,Y) means shared students require different slots. Revise(X,Y) removes x if no y in D(Y) satisfies x != y. After a domain shrinks, re-enqueue adjacent arcs. An empty domain means failure. Backtracking selects a smallest remaining domain and assigns a slot; propagation runs after each assignment.

Correctness: a value with no compatible neighbour value cannot appear in any valid complete assignment, so removing it cannot remove a solution. Arc consistency is not complete for all CSPs; backtracking is still needed. The four-exam cycle needed 6 decision nodes and 2 backtracks without propagation versus 1 decision and 0 backtracks with propagation (47 support checks); the baseline performed 24 direct constraint checks. A contradictory unary-domain example (P={1}, Q={1}, P!=Q) creates an empty domain before search. Domain states are returned in JSON; results/csp_domain_reduction.svg provides a schematic domain-shrink illustration.

## Source files and evidence
- Implementation: [assignment2.py](../assignment2.py)
- Experiment outputs: [results](../results/)
- Original brief: Unit 2.docx (Tasks 1–6 and Day-4 Task 7)
