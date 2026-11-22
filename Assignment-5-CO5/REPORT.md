# Assignment 5 – CO5
## Agents, Intelligent Systems and Real-Time AI: Architecture, Engineering and Deployment

**Course:** CSA17 – Artificial Intelligence  
**Nature:** Individual | **Total:** 50 marks  
**Student:** [Enter name]  
**Register number:** [Enter register number]  
**Repository:** https://github.com/Kishore-2008-05/CSA-1703-Artificial-Intelligence-

> This report follows the supplied Assignment 5 brief. Replace bracketed fields with your own details and insert screenshots/actual outputs from your own execution. The code currently generates synthetic demonstration data; do not describe it as a public dataset experiment.

# PART A – DESIGN AND REASONING

## A1 – Agent architecture: autonomous parcel-delivery drone (7 marks)

### A1.1 PEAS and environment
| PEAS element | Specification |
|---|---|
| Performance | Safe delivery, no-fly-zone avoidance, mission completion, low battery use, low delay |
| Environment | City grid, buildings, landing pads, weather/wind, obstacles, parcel destination |
| Actuators | Move north/south/east/west, hover, descend, return-to-base, emergency-land |
| Sensors | GPS, camera/LiDAR obstacle distance, IMU, wind estimate, battery, parcel/landing-pad status |

The environment is partially observable, stochastic, sequential, dynamic, continuous in physical motion but discretised to grid cells in the simulator, and multi-agent when other drones are present. A hybrid model-based and goal-based agent is needed to remember obstacles and current state and plan toward a destination. A utility layer ranks safe routes; a learning component may improve wind estimates but must not override safety rules. A simple reflex rule alone cannot plan around remembered obstacles.

### A1.2 Percepts, state and actions
Percepts: current position, detected obstacle cells, no-fly-zone map, wind vector, battery percentage, destination, nearby drone positions and landing-pad availability. Internal state: last known position, map belief, planned path, visited cells, battery estimate, active mission and emergency state. Actions: move one cell, hover, replan, return to a safe pad, or emergency-land.

### A1.3 Priority rule
Lexicographic arbitration: (1) collision/no-fly-zone safety, (2) emergency landing when battery is below the reserve threshold, (3) parcel delivery progress, (4) energy-efficient route. Safety constraints are hard constraints, not soft utility terms.

### A1.4 Hybrid sense–decide–act pseudocode
```text
ALGORITHM HYBRID_DRONE(percepts, state, goal)
BEGIN
  UPDATE state.position, state.battery, state.obstacle_map FROM percepts
  IF state.position is invalid OR sensor confidence is low THEN
      EXECUTE HOVER; REQUEST_SAFE_LOCALISATION
  ENDIF
  IF immediate obstacle intersects next motion cell OR next cell is no-fly THEN
      action ← EMERGENCY_BRAKE_OR_HOVER
      MARK cell blocked in state.obstacle_map
  ELSE IF state.battery ≤ RESERVE_THRESHOLD THEN
      safe_targets ← reachable safe landing pads
      IF safe_targets is empty THEN action ← EMERGENCY_LAND
      ELSE action ← first step on minimum-risk path to nearest safe target
      ENDIF
  ELSE
      path ← A_STAR(state.position, goal, state.obstacle_map, wind_cost)
      IF path is empty THEN action ← HOVER_AND_REQUEST_REPLAN
      ELSE action ← first safe step of path
      ENDIF
  ENDIF
  CHECK action against safety constraints
  EXECUTE action
  UPDATE state.position, state.visited, state.battery and mission status
  IF goal reached OR emergency landing completed THEN TERMINATE mission
  ELSE RETURN updated state
  ENDIF
END
```

### A1.5 Six-step hand trace
The simulator emits a reproducible six-step trace in `results/drone_trace.json`. The obstacle appears during the trace and battery decreases after movement. The trace records percept, previous position, battery, active decision layer and resulting position. Add a screenshot of the actual JSON output.

## A2 – Decentralised flood-search swarm (5 marks)

A central controller creates a single point of failure and requires continuous communication. Link loss can leave drones idle or repeating cells; controller failure can stop new assignments and reduce coverage. A decentralised drone selects an unvisited safe frontier using local obstacle information, neighbour positions and a shared/locally exchanged visit marker. Separation prevents collisions; a pheromone-like visit cost discourages redundant search.

**Per-agent pseudocode**
```text
ALGORITHM LOCAL_SWARM_STEP(agent, neighbours, local_map, visit_cost)
BEGIN
  UPDATE local_map FROM sensors AND neighbour messages
  candidates ← safe adjacent cells not occupied by neighbours
  IF battery ≤ reserve THEN RETURN nearest safe landing action
  IF candidates is empty THEN RETURN HOVER
  FOR each cell IN candidates DO
      score[cell] ← distance_to_frontier + visit_cost[cell]
                    + collision_penalty(cell, neighbours)
  ENDFOR
  chosen ← cell with minimum score
  BROADCAST chosen and local observations when link is available
  INCREASE visit_cost[chosen]
  RETURN MOVE chosen
END
```

A hand trace should show three agents moving on a 5×5 grid without central assignment. A failure case is a narrow corridor with two agents facing each other: both may repeatedly select the other's occupied cell and stall. A tie-break rule using drone ID and a timed back-off resolves the deadlock. The Python simulator is a simplified coverage model; its assumptions must be stated.

## A3 – Generic expert-system shell (5 marks)

### Domain rule examples
**Pump fault:** IF low pressure AND blocked filter THEN filter blockage; IF high temperature AND low flow THEN pump overheating; IF motor noise AND high vibration THEN bearing wear; IF no start AND power absent THEN power-supply fault.  
**Crop disease:** IF leaf spots AND humid weather THEN fungal disease; IF yellow leaves AND poor drainage THEN root stress; IF powdery coating THEN powdery mildew; IF chewed edges AND visible larvae THEN insect damage.  
**Flood triage:** IF trapped person AND rising water THEN highest priority; IF injury AND isolated location THEN urgent; IF safe shelter AND supplies available THEN routine; IF missing person AND last-seen zone flooded THEN urgent search.

Reusable shell components are the working memory, inference engine, rule matcher, conflict resolver and explanation facility. Domain-specific knowledge is stored as rules and labels, not hard-coded in the engine.

### Generic inference cycle
```text
ALGORITHM EXPERT_SYSTEM(KB, initial_facts)
BEGIN
  WM ← initial_facts
  REPEAT
    matches ← all rules whose premises are present in WM
    IF matches is empty THEN EXIT LOOP
    selected ← CONFLICT_RESOLUTION(matches, specificity, priority, recency)
    ADD selected conclusion to WM
    RECORD selected rule and supporting facts for explanation
  UNTIL goal reached OR no new fact can be added
  RETURN diagnosis, HOW explanation, WHY explanation
END
```

HOW lists rules/facts used to reach the conclusion. WHY explains why a question or fact is needed. Knowledge acquisition lets domain experts add/edit rules without changing inference-engine code; versioning and regression tests are required to avoid silently changing previous diagnoses.

## A4 – Distributed RDD pipeline (4 marks)

For records `(sensorId, timestamp, value)`:
1. `textFile` / input RDD creates partitions.
2. `map` to `(sensorId, (value, value, 1))` is a narrow transformation.
3. `reduceByKey` combines sum, max and count; it is a wide transformation and causes a shuffle by key.
4. `mapValues` computes mean and preserves max; narrow transformation.
5. `sortBy` or `takeOrdered(10)` obtains the ten noisiest sensors; ordering may require shuffle depending on implementation.
6. `collect` / `saveAsTextFile` is an action; lazy transformations execute only when an action is called.

Cache the parsed/cleaned RDD only if it is reused by multiple downstream actions. Caching a one-use intermediate wastes executor memory. RDD lineage records transformations and allows Spark to recompute lost partitions from source data. A production implementation and the required 10^5, 10^6 and 10^7 scaling runs need PySpark installed; record partition count, elapsed time, shuffle and cache observations from the actual cluster.

## A5 – Edge model design (4 marks)

Chosen case: synthetic intrusion detection. The demonstration uses a small centroid classifier as a transparent full model and quantises centroid values to a fixed precision for an edge variant. For a real neural model, parameter memory is approximately parameter_count × bytes_per_parameter; multiply-accumulate cost is approximately the sum of layer input×output dimensions per sample. The 50 ms limit must be measured on the target device, not inferred from a desktop run.

Compression pseudocode:
```text
OFFLINE:
  TRAIN full detector on training partition
  QUANTISE model weights/centroids to lower precision
  VALIDATE compressed model on untouched validation partition
ONLINE:
  EXTRACT features
  RUN compressed detector
  IF confidence is below threshold THEN request cloud review
  RETURN class and confidence
```
Quantisation reduces model storage and may improve cache use, but can reduce precision near class boundaries. Detect degradation with class-wise recall, F1, calibration and adversarial/noisy input tests.

# PART B – IMPLEMENTATION AND EXPERIMENTAL INVESTIGATION

## B1 – Drone and swarm implementation (7 marks)
Run `python assignment5.py --out results`. The program creates a six-step drone trace and swarm CSV for N=5, 10, 25 and 50, 30 deterministic seeds and simulated failure levels 0%, 10% and 30%. The current baseline is a grid-world teaching simulator, not a flight controller. Review generated coverage, mission completion, redundancy and battery metrics. Add scenario screenshots and discuss any mismatch between the manual trace and program trace.

## B2 – Adversarial expert system (5 marks)
The program includes a reusable rule evaluator and a 15-rule pump-fault knowledge base. It generates a 15/15 development/hold-out demonstration from repeated synthetic templates. This is only a smoke test: it does **not** satisfy the brief's requirement for 30 independently expert-labelled cases or a meaningful per-fault evaluation. Extend the case file with genuine labelled cases, then report per-fault precision/recall, rule firings, conflicting rules, missing-evidence cases, specificity/priority/recency comparisons and runtime rule-edit regression.

## B3 – Full versus edge applied case (8 marks)
The included intrusion-like dataset is generated synthetically with a seeded random generator. It demonstrates a leakage-aware train/test workflow and compares full-precision and quantised centroids, recording accuracy, precision, recall, F1, confusion matrix, latency, throughput and serialized model size. It is not a public benchmark. For final marks, replace it with an instructor-approved public intrusion dataset and cite its source; use a chronological split if records are time ordered. Categorise at least five false predictions. Run PySpark at 10^5, 10^6 and 10^7 rows with 1, 2, 4 and 8 partitions and record cache/shuffle counts. Measure on the target edge device and report mean and p95 latency.

## B4 – Conversational interface and deployment (5 marks)
The baseline chatbot defines eight intents and a confidence-threshold fallback. Its smoke tests are not a full evaluation. Add a labelled test set, then compute per-intent precision/recall/F1, confusion matrix and response latency. Simulate speech transcription errors at 0%, 10%, 20% and 30% word-error rates; report intent accuracy, out-of-scope detection and false accepts. Sweep the threshold and plot the resulting trade-off.

## Engineering conclusion
Use edge inference when the measured p95 latency, privacy and connectivity requirements justify local processing and the compressed model retains acceptable class-wise recall. Use cloud inference when model size, update frequency or compute demand exceeds device limits, provided network latency and data governance are acceptable. A hybrid design can keep urgent screening local and send uncertain cases to the cloud. Reverse the decision when measured latency, cost, throughput, privacy constraints or error rates change.

## Reproducibility and evidence checklist
- [ ] Add student name, register number, Python version and machine details.
- [ ] Execute the program and commit the generated `results/` files.
- [ ] Add screenshots of command, logs and metric tables.
- [ ] Replace synthetic benchmark with an instructor-approved public dataset and cite it.
- [ ] Complete independent 30-case expert labels and adversarial rule-order tests.
- [ ] Run PySpark scaling and caching experiments on an available Spark setup.
- [ ] Complete speech-error and chatbot threshold experiments.
- [ ] State limitations and never present simulated data as real-world measurements.
