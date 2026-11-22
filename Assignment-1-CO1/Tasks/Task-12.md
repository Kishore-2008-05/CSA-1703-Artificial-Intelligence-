# Assignment 1 – CO1 | Task 12

## Task 12 – Sensor/localisation failure
The robot no longer knows one exact start vertex; its information state is a belief set of k candidate junctions. There can be up to 2^V possible belief subsets. **Decision: modify** the design: use local sensing/odometry to reduce the candidate set, then run UCS from the identified junction. Without sensing, a safe conditional policy must work from every candidate and may be much more expensive or impossible. results/belief_states.json records the subset upper bound for k=2,4,8 and a simple action proxy with/without a local sensor. This is an illustrative model, not a physical robot test.

## Source files and evidence
- Implementation: [assignment1.py](../assignment1.py)
- Experiment outputs: [results](../results/)
- Original brief: Unit 1.docx (Tasks 1–11 and Day-4 Task 12)
