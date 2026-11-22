# CSA17 – Artificial Intelligence (CSA-1703)

This repository contains the working material for **Assignment 1 (CO1)** and **Assignment 2 (CO2)**, based on the two assignment briefs supplied for this course.

- **Language:** Python 3
- **Recommended environment:** Jupyter Notebook / Google Colab / local Python
- **Assignment 1:** Hospital Medicine-Delivery Robot (Tasks 1–11 and Day-4 Task 12)
- **Assignment 2:** Searching Techniques (Tasks 1–6 and Day-4 Task 7)

> **How to use this repository:** Start with this README for navigation. Read the relevant `REPORT.md` for the connected explanation, open the individual task file for a task-wise view, and use the Python file and `results/` folder for implementation and experiment evidence.

---

## 1. Assignment 1 – CO1: Hospital Medicine-Delivery Robot

**Problem:** Model a hospital as a graph. The robot must find a route from the pharmacy to a ward while considering travel costs and increasing graph size.

### Files and folders

| File / folder | What it contains |
|---|---|
| [Assignment 1 report](Assignment-1-CO1/REPORT.md) | Combined explanation for Tasks 1–12: agent design, algorithms, complexity, experiments, recommendation and sensor-failure redesign. |
| [Task-wise answers](Assignment-1-CO1/Tasks/) | Separate Markdown files for Task 1 through Task 12. |
| [Python implementation](Assignment-1-CO1/assignment1.py) | Graph generation and implementations of BFS, Uniform-Cost Search and recursive Depth-Limited Search, with experiment routines. |
| [Raw results and test data](Assignment-1-CO1/results/) | CSV/JSON experiment records and generated graph files. |

### Task guide

1. [Task 1 – Agent and search-algorithm design](Assignment-1-CO1/Tasks/Task-01.md): PEAS, environment classification, problem formulation and three distinct uninformed search strategies.
2. [Task 2 – Basic operation](Assignment-1-CO1/Tasks/Task-02.md): identify the main operation counted for each algorithm.
3. [Task 3 – Mathematical time and space analysis](Assignment-1-CO1/Tasks/Task-03.md): derive search and preprocessing costs.
4. [Task 4 – Best, average and worst cases](Assignment-1-CO1/Tasks/Task-04.md): explain how input conditions affect the amount of search.
5. [Task 5 – Asymptotic analysis](Assignment-1-CO1/Tasks/Task-05.md): compare growth as the hospital graph becomes larger.
6. [Task 6 – Recurrence formulation](Assignment-1-CO1/Tasks/Task-06.md): derive the recursive search recurrence.
7. [Task 7 – Recurrence solution](Assignment-1-CO1/Tasks/Task-07.md): solve and interpret the recurrence, including iterative deepening.
8. [Task 8 – Implementation and testing](Assignment-1-CO1/Tasks/Task-08.md): Python implementation, generated graphs and test cases.
9. [Task 9 – Experimental performance](Assignment-1-CO1/Tasks/Task-09.md): operation counts, frontier/memory proxy, path information, timings, tables and graphs.
10. [Task 10 – Theory versus experiment](Assignment-1-CO1/Tasks/Task-10.md): interpret whether measured growth follows the theoretical analysis.
11. [Task 11 – Final recommendation](Assignment-1-CO1/Tasks/Task-11.md): defend the recommended search strategy for weighted hospital routes.
12. [Task 12 – Day-4 sensor-failure challenge](Assignment-1-CO1/Tasks/Task-12.md): reconsider the design when the robot has a set of possible current locations rather than one known location.

### Run Assignment 1

Open a terminal in the Assignment 1 folder and run:

```bash
cd Assignment-1-CO1
python assignment1.py
```

The script writes or refreshes its experiment outputs in the `results/` folder. See the report for the meaning of each result file and the experiment limitations.

---

## 2. Assignment 2 – CO2: Searching Techniques

**Problem:** Investigate informed and online search, game-tree search, constraint propagation, combinatorial optimisation and a computational redesign.

### Files and folders

| File / folder | What it contains |
|---|---|
| [Assignment 2 report](Assignment-2-CO2/REPORT.md) | Combined explanation for Tasks 1–7, including the Day-4 redesign. |
| [Task-wise answers](Assignment-2-CO2/Tasks/) | Separate Markdown files for Task 1 through Task 7. |
| [Python implementation](Assignment-2-CO2/assignment2.py) | Grid search, online DFS, minimax/alpha-beta, CSP, exhaustive TSP, 2-opt and move-ordering prototype. |
| [Raw results and test data](Assignment-2-CO2/results/) | CSV/JSON experiment records and generated graph files. |

### Task guide

1. [Task 1 – UCS, Greedy Best-First and A*](Assignment-2-CO2/Tasks/Task-01.md): compare search on different grid-map layouts and justify the Manhattan heuristic.
2. [Task 2 – Online search agent](Assignment-2-CO2/Tasks/Task-02.md): examine exploration moves, revisits, competitive ratio and when mapping once is better than repeated online exploration.
3. [Task 3 – Alpha-beta pruning](Assignment-2-CO2/Tasks/Task-03.md): compare minimax and alpha-beta under different child-ordering conditions.
4. [Task 4 – Minimax and evaluation functions](Assignment-2-CO2/Tasks/Task-04.md): derive game-tree growth and discuss the cost of deeper lookahead.
5. [Task 5 – Constraint propagation and CSP](Assignment-2-CO2/Tasks/Task-05.md): represent exam-timetabling constraints, remove unsupported values and combine propagation with backtracking.
6. [Task 6 – Exhaustive and local search](Assignment-2-CO2/Tasks/Task-06.md): compare exhaustive delivery-tour enumeration with a 2-opt local-search method.
7. [Task 7 – Day-4 redesign challenge](Assignment-2-CO2/Tasks/Task-07.md): diagnose a bottleneck, define an objective, redesign the strategy, predict, test and defend the result.

### Run Assignment 2

Open a terminal in the Assignment 2 folder and run:

```bash
cd Assignment-2-CO2
python assignment2.py
```

The script writes or refreshes its experiment outputs in the `results/` folder. See the report for the meaning of each result file and the experiment limitations.

---

## 3. Understanding the evidence folders

The `results/` folders contain supporting experiment outputs. Depending on the task, these include:

- **CSV files:** row-by-row measurements that can be opened in Excel.
- **JSON files:** test-case details, experiment summaries and recorded measurements.
- **SVG files:** graphs that can be opened in a browser or inserted into a report.

For the exact interpretation of each result, refer to the matching task and the relevant report section. The Python source is the implementation reference; the CSV/JSON files are the recorded data; the report explains what the measurements mean.

## 4. Important notes before submission

1. The assignment brief requires a complete evidence chain for implemented tasks: **source code → test input → expected behaviour → actual output → performance metrics → interpretation**.
2. Predictions requested by the brief should be written before running the experiment. Keep the prediction separate from the observed result.
3. Operation counts (such as nodes expanded, generated nodes, frontier size, constraint checks and evaluation calls) are primary evidence. Execution time is supplementary and depends on the computer used.
4. The experiments in this repository use generated/synthetic teaching examples. They are not measurements from a real hospital, campus shuttle, rover, commercial game or university timetable.
5. Re-run the Python scripts on your own computer and retain the resulting output files. If your run produces different timings or counts, use your own reproducible output in the final submission and update the report accordingly.
6. Read and understand the algorithms and results before submission. You may be asked to explain the design, code, test inputs, predictions and conclusions in a viva.

## 5. Suggested submission order

For each assignment, submit or package:

1. The combined report (`REPORT.md`, or an exported PDF/DOCX if your instructor requires that format).
2. The Python source file.
3. The relevant raw CSV/JSON result files.
4. The graphs used in the discussion.
5. The task-wise Markdown files as supporting, easy-to-navigate explanations.

---

**Repository:** [Kishore-2008-05 / CSA-1703-Artificial-Intelligence-](https://github.com/Kishore-2008-05/CSA-1703-Artificial-Intelligence-)
