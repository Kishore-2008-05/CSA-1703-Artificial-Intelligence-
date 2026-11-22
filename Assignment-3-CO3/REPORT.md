# Assignment 3 – CO3: Logical Agents and First-Order Reasoning
**Course:** CSA17 Artificial Intelligence | **Marks:** 50 | **Mode:** Pair work

## Overview
This report organises the seven assignment tasks around knowledge representation, entailment, resolution, first-order logic, unification and rule-based inference. The accompanying `logic_lab.py` provides compact, runnable educational implementations. It is a starting implementation and must be extended with the full experimental matrices and proof artefacts required by the brief.

## Task 1 – Logical agents, Wumpus-world KB and inference patterns
Represent each square with propositional symbols for pit, wumpus, breeze and stench. For a square (i,j), the breeze rule is `B_ij ↔ (P_(i-1,j) ∨ P_(i+1,j) ∨ P_(i,j-1) ∨ P_(i,j+1))`, omitting neighbours outside the grid. Stench is analogous for adjacent Wumpus locations. A grid with n² squares has O(n²) percept/hazard symbols; the number of truth assignments for m symbols is 2^m. A query should enumerate only symbols on which its KB fragment depends when sound variable elimination is possible. Model checking is sound when it reports entailment only if every KB model satisfies the query; it is complete when every entailed query is eventually reported.

The source includes a finite truth-table checker. Extend the toy 2×2 example to n=2,3,4, log models examined, KB evaluations and time, and compare full enumeration with a query-relevant symbol subset. Test an entailed query, a contradicted query and an unknown query. For the same safety facts, derive at least two conclusions using Modus Ponens, And-Elimination and Unit Resolution; record inference steps and provide truth tables showing each rule preserves truth.

## Task 2 – Model checking versus propositional resolution
Create a smart-building policy with at least ten rules covering valid badge, time window, visitor status, escort requirement and emergency override. Include implication, biconditional and disjunction. Convert formulas to CNF by eliminating biconditionals/implications, pushing negations inward and distributing OR over AND. Resolution refutes KB ∧ ¬query. The provided resolution function is a small CNF demonstration; extend it with canonical clause storage, tautology deletion, subsumption and a step cap. Compare model counts with attempted resolvents on implication chains of length 10, 20, 40 and 80 and on at least two structurally different KB families. Resolution termination without an empty clause means no proof was found within the finite propositional closure; for a non-entailed query, explain the saturation condition.

## Task 3 – Knowledge engineering in first-order logic
For an exam eligibility advisor, use predicates such as Student(s), Course(c), Attendance(s,c,p), PrerequisiteCleared(s,c), FeesPaid(s), Disciplined(s), ApprovedLeave(s,c), and Eligible(s,c). Encode general regulations once with quantified axioms and student/course facts separately. Include an existential rule such as ∃s Student(s) ∧ Eligible(s,AI101). A propositional encoding repeats rules per student/course and therefore grows with the number of student-course pairs (O(sc)); a first-order rule set remains approximately constant while the facts grow with the domain. Design at least 15 competency queries: five true, five false and five returning bindings. Track at least three defects and fixes, and measure KB size/inference time as s and c grow. Greater expressiveness does not guarantee faster inference: unification and search may dominate for small domains.

## Task 4 – Unification and lifted inference
The source implements recursive unification for constants, variables and tuple terms, including an occurs check. A most general unifier (MGU) is a substitution that makes two terms identical while imposing no unnecessary bindings. Test five hand-designed pairs, including an occurs-check failure such as `?x = f(?x)` and a standardise-apart example where two clauses' local variables must be renamed before unification. Lifted Modus Ponens applies substitutions to variables without first generating every ground instance. Measure ground-clause counts for 3–30 constants and increasing predicate arity; introduce a function symbol and report term growth by depth bound. Propositionalisation may still be practical for tiny finite domains, fixed queries or systems requiring a simple ground engine.

## Task 5 – First-order resolution
Translate the employee/document statements into predicates:
- Handles(e,d) ∧ Restricted(d) → Authorised(e)
- PatientData(d) → Restricted(d)
- ∃e ∀d (Audited(d) → Handles(e,d))
- PatientData(R1) and Audited(R1)

Skolemise the existential employee with a constant (e.g. e0), convert to CNF and use the Task 4 unifier in resolution refutation to prove ∃e Authorised(e). Show each clause and resolvent in the report. Compare unit preference or set-of-support against an unprioritised strategy. Also run a non-entailed query with a step cap; first-order resolution is semi-decision: proofs can be found when entailed, but failure to find a proof does not generally certify non-entailment.

## Task 6 – Forward and backward chaining
Use a definite-clause organisation hierarchy with about ten rules and datasets of 100, 1,000 and 10,000 facts. Forward chaining repeatedly fires applicable rules to a fixed point; log inferred facts, firings, redundant derivations, iterations and query-irrelevant facts. Backward chaining starts from a query and recursively proves its subgoals; log expanded goals, unifications, maximum depth and repeated goals. Demonstrate a left-recursive rule and prevent nontermination with loop checking, depth limits or memoisation. The source contains a ground-atom prototype with cycle detection; extend it to variable substitutions for the full task.

## Task 7 – Day-4 design challenge: hospital medication-safety advisor
Use a first-order, rule-based representation for patients, medicines, allergies, conditions and prescriptions. A backward-chaining query can focus work on one proposed prescription; an agenda/index should select only rules relevant to the queried drug and patient. Attach provenance to each fired rule so the system can explain why it flags a prescription. The code includes explicitly labelled toy rules and must not be used for real clinical decisions.

Pair design must include two independent initial proposals, a comparison, a joint final architecture, complete pseudocode, theoretical validation and at least 30 test cases over 40, 400 and 2,000 rules. Report query latency, inference steps, memory and explanation length. Include dangerous combinations and baseline comparison. Discuss uncertainty, missing records and the limits of a purely logical representation.

## Pair contribution record
Fill this table with the actual names and work performed. Both partners must understand every task.

| Task | Student A – primary contribution | Student B – primary contribution | Joint work |
|---|---|---|---|
| 1–7 | **Fill in actual work** | **Fill in actual work** | **Fill in actual collaboration** |

## Reproducibility
Run `python logic_lab.py`. The printed outputs are small sanity checks, not a substitute for the full 100/1,000/10,000-fact and 30-case experiments. Keep raw CSV data, test inputs, proof traces and plots with the final report. Operation counts are primary; time is secondary.
