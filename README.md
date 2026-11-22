# CSA17 – Artificial Intelligence (CSA-1703)
## Assignment Portfolio: CO1 and CO2

**Course:** CSA17 – Artificial Intelligence  
**Assignments covered:** Assignment 1 (CO1) and Assignment 2 (CO2)  
**Programming language:** Python 3  
**Suggested environment:** Jupyter Notebook, Google Colab, or a local Python installation  
**Repository owner:** Kishore-2008-05

---

## 1. Project overview

This repository organises the implementation and written work for two individual Artificial Intelligence assignments. The assignments investigate how an intelligent agent searches for solutions, how search algorithms behave as problem size increases, and how computational evidence can be used to justify an engineering decision.

The work is divided into two scenarios:

1. **Assignment 1 – CO1: Hospital Medicine-Delivery Robot.** A robot must navigate a hospital graph from a pharmacy to a requested ward. The assignment focuses on intelligent-agent design, problem formulation, uninformed search, mathematical complexity, implementation, performance measurement and a changed requirement in which the robot's exact location is unknown.
2. **Assignment 2 – CO2: Searching Techniques.** A campus shuttle, exploration rover, game-playing agent, university timetable solver and delivery-tour planner provide different contexts for studying informed search, online search, minimax, alpha-beta pruning, constraint propagation, exhaustive search and local optimisation. The final task asks for a measured redesign of one computational bottleneck.

The purpose is not only to run standard algorithms. Each assignment asks the student to **predict, design, implement, measure, analyse, evaluate and defend** a solution.

### Repository navigation

| Resource | Purpose |
|---|---|
| [Assignment 1 – complete report](Assignment-1-CO1/REPORT.md) | Consolidated written discussion for CO1 Tasks 1–12. |
| [Assignment 1 – task files](Assignment-1-CO1/Tasks/) | Individual Markdown explanations for each CO1 task. |
| [Assignment 1 – Python source](Assignment-1-CO1/assignment1.py) | Search implementations and generated hospital-graph experiments. |
| [Assignment 1 – results](Assignment-1-CO1/results/) | CSV/JSON evidence and SVG figures for CO1. |
| [Assignment 2 – complete report](Assignment-2-CO2/REPORT.md) | Consolidated written discussion for CO2 Tasks 1–7. |
| [Assignment 2 – task files](Assignment-2-CO2/Tasks/) | Individual Markdown explanations for each CO2 task. |
| [Assignment 2 – Python source](Assignment-2-CO2/assignment2.py) | Informed/online search, game-tree, CSP and optimisation prototypes. |
| [Assignment 2 – results](Assignment-2-CO2/results/) | CSV/JSON evidence and SVG figures for CO2. |

---

# 2. Assignment 1 – CO1
## Design, Analyse and Validate an Efficient Search Strategy for a Hospital Medicine-Delivery Robot

### 2.1 Problem description

A multi-block hospital is represented as a graph. Vertices represent locations such as junctions, corridors, lifts and ward doors. Edges represent possible movements between connected locations, and each edge has a travel-time cost. The robot starts at the central pharmacy and must reach a requested ward.

As hospital buildings grow, the assignment asks the designer to consider state spaces of approximately **1,000, 10,000, 100,000 and 1,000,000 states**. The route planner should be correct and practical, and preprocessing costs such as adjacency-list construction and duplicate detection must be included in the analysis.

### 2.2 Agent and problem design

The report begins by defining the robot using the PEAS framework:

- **Performance measure:** deliver the correct medicine to the correct ward, avoid unsafe routes, reduce travel time and unnecessary movement, and use resources efficiently.
- **Environment:** hospital pharmacy, corridors, junctions, lifts, ward entrances, people and possible route restrictions.
- **Actuators:** wheels or motors, lift/door controls where available, and the medicine-delivery compartment.
- **Sensors:** localisation, obstacle detection, corridor/lift status and other information needed to determine the robot's position and surroundings.

The search problem is then represented using states, an initial state, actions, a transition model, a goal test and a path-cost function. The graph model makes the locations discrete even though the physical robot moves continuously. The environment classification and rational-agent discussion are explained in the CO1 report.

### 2.3 Search strategies investigated

The implementation and report discuss three different uninformed search approaches:

1. **Breadth-First Search (BFS):** uses a first-in-first-out queue and explores by increasing number of edges. It is useful as a minimum-hop baseline when every movement has equal cost.
2. **Uniform-Cost Search (UCS):** uses a priority queue ordered by accumulated path cost. With non-negative edge costs, it finds a least-cost route and is therefore relevant when hospital corridors have different travel times.
3. **Recursive Depth-Limited Search (DLS):** explores recursively up to a selected depth limit. It demonstrates recursive search and lower path/stack storage, but it is not complete when the goal lies beyond the limit and does not guarantee a minimum-cost route.

The report also identifies the basic operation for each method, derives time and space expressions, discusses best/average/worst cases, and formulates and solves a recurrence for the recursive method.

### 2.4 Task-by-task coverage

| Task | Main topic | What the task explanation covers |
|---|---|---|
| [Task 1](Assignment-1-CO1/Tasks/Task-01.md) | Agent and algorithm design | PEAS, environment classification, rationality, problem formulation, three distinct uninformed approaches, pseudocode and preprocessing. |
| [Task 2](Assignment-1-CO1/Tasks/Task-02.md) | Basic operation | The dominant operation in each algorithm and why counting it helps analyse execution work. |
| [Task 3](Assignment-1-CO1/Tasks/Task-03.md) | Mathematical complexity | Derivation using branching factor, goal depth, maximum depth, optimal cost and minimum step cost; frontier and preprocessing costs. |
| [Task 4](Assignment-1-CO1/Tasks/Task-04.md) | Best, average and worst cases | How goal position, unreachable goals, branch order and edge costs change the search effort. |
| [Task 5](Assignment-1-CO1/Tasks/Task-05.md) | Asymptotic analysis | O, Ω and Θ growth and the practical effect of increasing the hospital graph. |
| [Task 6](Assignment-1-CO1/Tasks/Task-06.md) | Recurrence formulation | A recurrence derived from the recursive search, including subproblem size, recursive calls, local work and base case. |
| [Task 7](Assignment-1-CO1/Tasks/Task-07.md) | Recurrence solution | Step-by-step solution and interpretation, including the repeated work in iterative deepening. |
| [Task 8](Assignment-1-CO1/Tasks/Task-08.md) | Implementation and testing | Python implementation, consistent graph inputs, seeds, reachable/unreachable cases and start-equals-goal testing. |
| [Task 9](Assignment-1-CO1/Tasks/Task-09.md) | Performance measurement | Generated/expanded nodes, maximum frontier, route depth/cost, optimality and repeated timing measurements, with tables/graphs. |
| [Task 10](Assignment-1-CO1/Tasks/Task-10.md) | Theory versus experiment | Whether measured operation counts and frontier sizes follow the theoretical growth and why differences can occur. |
| [Task 11](Assignment-1-CO1/Tasks/Task-11.md) | Final recommendation | A recommendation justified by route-cost requirements, theoretical analysis, experimental evidence and limitations. |
| [Task 12](Assignment-1-CO1/Tasks/Task-12.md) | Day-4 sensor-failure challenge | Belief-state representation, possible starting locations, the possible 2^V belief-state space, local sensing and a revised design. |

### 2.5 Implementation and outputs

The main implementation is [assignment1.py](Assignment-1-CO1/assignment1.py). It contains BFS, UCS, recursive DLS and seeded graph generation. It records test cases and scaling measurements.

The [results folder](Assignment-1-CO1/results/) contains:

- `scaling.csv` – recorded search measurements across generated graph sizes.
- `test_cases.json` – selected correctness test cases and their outputs.
- `belief_states.json` – illustrative belief-state counts and a simple local-sensor comparison.
- `nodes_expanded.svg` and `runtime.svg` – figures for comparing search effort and elapsed time.

### 2.6 Day-4 design challenge

The original problem assumes that the robot knows its exact starting vertex. The changed requirement removes that assumption: after a restart or sensor failure, the robot knows only that it is at one of several possible junctions.

The robot's information must therefore be represented as a **belief state** (a set of possible locations), rather than one known vertex. With V possible locations, the number of possible subsets is at most 2^V. The design discussion considers whether to retain, modify or redesign the original approach, and explains how local sensing can reduce uncertainty before route planning.

### 2.7 Run Assignment 1

From a terminal opened in the repository:

```bash
cd Assignment-1-CO1
python assignment1.py
```

The script writes its experiment outputs to the `results/` directory. Open the report and task files alongside the source code to understand the inputs, measurements and interpretation.

---

# 3. Assignment 2 – CO2
## Searching Techniques: Informed Search, Online Search, Game Playing, CSP and Optimisation

### 3.1 Problem description

The second assignment investigates several search problems rather than one single scenario. It asks how an algorithm's behaviour changes with the map layout, available information, branching structure, constraints and size of the solution space.

The tasks cover:

- Uniform-Cost Search, Greedy Best-First Search and A*.
- Online exploration in an unmapped facility.
- Minimax and alpha-beta pruning.
- Depth-limited minimax and evaluation functions.
- Constraint propagation for exam timetabling.
- Exhaustive and local search for a delivery-tour problem.
- Diagnosis, redesign and validation of a computational bottleneck.

### 3.2 Task-by-task coverage

| Task | Main topic | What the task explanation covers |
|---|---|---|
| [Task 1](Assignment-2-CO2/Tasks/Task-01.md) | UCS, Greedy and A* on grid maps | Predictions, an admissible Manhattan heuristic, contrasting map layouts, node/frontier/path metrics and a recommendation for the stated open-road operating profile. |
| [Task 2](Assignment-2-CO2/Tasks/Task-02.md) | Online search agent | Online DFS exploration, target distance, unreachable targets, maze size, dead-end density, revisited cells and competitive ratio against an offline shortest-path reference. |
| [Task 3](Assignment-2-CO2/Tasks/Task-03.md) | Alpha-beta pruning | Designed game trees, move ordering, predictions, node visits, cutoffs and comparison with minimax. |
| [Task 4](Assignment-2-CO2/Tasks/Task-04.md) | Minimax and evaluation functions | Mathematical game-tree growth, depth limits, terminal evaluations, a student-defined evaluation function and response-time considerations. |
| [Task 5](Assignment-2-CO2/Tasks/Task-05.md) | Constraint propagation and CSP | Variables, domains, constraints, unsupported-value removal, arc rechecking, domain wipe-out, backtracking and correctness reasoning. |
| [Task 6](Assignment-2-CO2/Tasks/Task-06.md) | Exhaustive and local search | Candidate-tour generation, factorial growth, checking a small optimum, 2-opt local search, quality gap and a deployment boundary. |
| [Task 7](Assignment-2-CO2/Tasks/Task-07.md) | Day-4 diagnose, redesign and validate | Computational bottleneck, measurable design objective, revised strategy, prediction, implementation comparison and defence of the final design. |

### 3.3 Main algorithms and engineering ideas

**Informed grid search:** The code compares UCS, Greedy Best-First Search and A*. The Manhattan-distance heuristic is appropriate for a four-direction grid with unit movement cost. It estimates the distance in a relaxed map without obstacles; obstacles cannot make the true shortest route shorter than that relaxed distance. Greedy uses only the heuristic and may choose a non-optimal path, while A* combines the cost already travelled with the estimated remaining cost.

**Online exploration:** The rover does not have a complete map in advance. It senses nearby cells, explores and backtracks. The analysis compares online movement with an offline shortest-path reference and discusses why repeated missions in a stable facility may justify mapping first and planning offline.

**Game-tree search:** Minimax examines possible moves for two opposing players. Alpha-beta pruning can avoid examining branches that cannot affect the final decision. The number of cutoffs depends strongly on the order in which moves are explored, not only on tree depth and branching factor.

**Constraint propagation:** The exam-timetabling problem represents exams as variables and available time slots as domains. A value can be removed when a neighbouring variable has no compatible supporting value. When a domain becomes empty, the current branch fails. Propagation is combined with backtracking because local consistency alone does not guarantee that every CSP has a complete solution.

**Combinatorial optimisation:** Exhaustive delivery-tour search enumerates possible tours and retains the best one. The number of tours grows factorially as customers are added. A 2-opt local-search method can improve a tour by reversing sections of its route, but it may stop at a local optimum rather than finding the global optimum.

**Redesign:** The final task requires the student to select a real limitation from the earlier experiments, identify the expensive or repeated operation, set a measurable objective, propose a reasoned change, predict its effect and compare the original and redesigned implementations under equivalent conditions.

### 3.4 Implementation and outputs

The main implementation is [assignment2.py](Assignment-2-CO2/assignment2.py). It contains prototypes for grid search, online DFS, minimax and alpha-beta, constraint propagation, exhaustive TSP and 2-opt local search.

The [results folder](Assignment-2-CO2/results/) contains:

- `grid_search.csv` – search measurements for the different grid-map conditions.
- `experiments.json` – recorded experiment summaries for game-tree, CSP, optimisation and other task demonstrations.
- `tsp_local_runs.csv` – recorded local-search run data.
- `online_dfs_experiments.csv` – online exploration runs, where generated by the current script/version.
- `grid_expansions.svg`, `tsp_growth.svg` and `csp_domain_reduction.svg` – visual summaries of selected experiments.

Check the actual files present in the folder before packaging the submission. The Python source and the raw outputs should be kept together so that the results can be traced to the implementation that produced them.

### 3.5 Run Assignment 2

From a terminal opened in the repository:

```bash
cd Assignment-2-CO2
python assignment2.py
```

The script writes or refreshes the experiment outputs in the `results/` directory. Review the generated files after each run.

---

# 4. Experimental method and evidence standard

The assignment briefs specify a common evidence chain for implemented tasks:

**Source code → Test input → Expected behaviour → Actual output → Performance metrics → Interpretation**

This means that a final screenshot or a program's final answer alone is not sufficient. The report should explain what was tested, what the student expected to happen, what actually happened and what the measurements show.

### 4.1 Metrics to prioritise

Depending on the algorithm, useful primary measurements include:

- Nodes generated and nodes expanded.
- Maximum frontier size or another memory-use proxy.
- Path length, path cost and whether the result is optimal.
- Number of revisited cells and competitive ratio for online exploration.
- Number of alpha-beta cutoffs and game-tree nodes visited.
- Constraint checks, domain reductions, search nodes, backtracks and domain wipe-outs.
- Number of candidate tours, local-search cost and percentage gap from a known optimum.
- Evaluation-function calls for game-tree experiments.

Execution time can be recorded, but it is affected by the computer, interpreter, background processes and implementation details. Operation counts are therefore important when comparing algorithm behaviour.

### 4.2 Predictions and repeatability

When a task asks for a prediction, write it down **before** running the experiment. Use fixed random seeds where appropriate, record the test input and use equivalent conditions when comparing algorithms. Where the brief asks for repeated runs, report the number of runs and the average or other appropriate summary.

### 4.3 Interpreting the results

Do not only paste tables. Explain why an algorithm expanded more nodes, why a frontier became larger, why a heuristic was or was not useful, why pruning occurred, or why a local-search result differed from the optimum. Connect the observations to the mathematical analysis and to the operating scenario.

---

# 5. Important limitations and submission checks

1. The maps, graphs, game trees, timetables and delivery-tour examples in this repository are **synthetic teaching examples**. They are not measurements from a real hospital, campus, rover, game engine or university timetable.
2. Runtime measurements depend on the computer used. Re-run the scripts in your own environment and retain the outputs produced by that run.
3. Treat the report's numerical tables and graphs as recorded project material that must be checked against a fresh run of the current Python source before final submission. If the output differs, update the report to match your reproducible output.
4. Check that every file named in the report is actually present in the relevant `results/` folder after running the code.
5. The assignment asks for predictions, test inputs, expected behaviour, actual output, performance metrics and interpretation. Make sure these are all included for each implemented task that requires evidence.
6. Read and understand the code and conclusions. The assignment briefs state that students may be asked to explain their algorithm design, test data, predictions, measurements and conclusions during a viva.
7. Follow the instructor's required submission format. Markdown files can be viewed on GitHub and can be exported or converted if a PDF or DOCX report is required.

---

# 6. Suggested final submission package

For **each assignment**, organise the final submission in this order:

1. **Complete report:** the relevant `REPORT.md`, exported to the format requested by the instructor.
2. **Task-wise explanations:** the Markdown files in the assignment's `Tasks/` folder.
3. **Source code:** the corresponding Python implementation.
4. **Raw experimental data:** the CSV and JSON files generated by the final verified run.
5. **Tables and graphs:** the figures actually used to support the report's discussion.
6. **Reproducibility details:** Python version, random seeds, test conditions and the command used to run the code.

### Final checklist

- [ ] I have read the original assignment brief and checked every task requirement.
- [ ] I have run the correct Python file successfully.
- [ ] I have checked that the output files were generated and correspond to the current code.
- [ ] I have included predictions before the relevant experiments.
- [ ] I have explained the measurements rather than only copying the numbers.
- [ ] I can explain the algorithms, complexity, test cases and design decisions in my own words.
- [ ] I have exported the report to the file format required by my instructor.

---

## 7. Repository link

[Open the CSA17 Artificial Intelligence GitHub repository](https://github.com/Kishore-2008-05/CSA-1703-Artificial-Intelligence-)

**End of README**


---

# 8. Assignment 3 – CO3: Logical Agents and First-Order Reasoning

[Open Assignment 3 folder](Assignment-3-CO3/)

- [Detailed report](Assignment-3-CO3/REPORT.md)
- [Task-wise explanations](Assignment-3-CO3/Tasks/)
- [Python logic implementations](Assignment-3-CO3/logic_lab.py)
- [Assignment instructions and run guide](Assignment-3-CO3/README.md)

This pair assignment covers Wumpus-world knowledge bases, truth-table entailment, propositional resolution, first-order knowledge engineering, unification, lifted inference, first-order resolution, forward/backward chaining and a hospital medication-safety advisor. Complete the contribution record with the actual two students' names and work.

# 9. Assignment 4 – CO4: Learning Algorithms

[Open Assignment 4 folder](Assignment-4-CO4/)

- [Detailed report](Assignment-4-CO4/REPORT.md)
- [Task-wise explanations](Assignment-4-CO4/Tasks/)
- [Python learning implementations](Assignment-4-CO4/learning_lab.py)
- [Assignment instructions and run guide](Assignment-4-CO4/README.md)

This individual assignment covers learning-protocol validation, decision trees, Gaussian-mixture EM, neural-network backpropagation, Naive Bayes, SVMs, explanation-based learning and reinforcement learning.

**Submission note:** The new folders contain design/report material and runnable teaching prototypes. Re-run and extend the experiments to satisfy every required dataset size, seed count, comparison, trace and graph in the original briefs before final submission.


## 10. Assignment 5 – CO5: Agents, Intelligent Systems and Real-Time AI

- [Assignment 5 folder](Assignment-5-CO5/)
- [Assignment 5 report](Assignment-5-CO5/REPORT.md)
- [Runnable Python baseline](Assignment-5-CO5/assignment5.py)
- [Setup and run instructions](Assignment-5-CO5/README.md)

This package includes a hybrid drone/grid simulator, decentralised swarm experiments, an expert-system rule engine, a synthetic edge-model comparison and an eight-intent retrieval chatbot. See the Assignment 5 README and report for limitations and additional experiments still required by the rubric. Synthetic data are clearly labelled and must not be reported as public-dataset evidence.
