# Assignment 4 – CO4: Learning Algorithms – Design, Implementation, Test and Evaluation
**Course:** CSA17 Artificial Intelligence | **Mode:** Individual | **Total:** 50 marks

## Engineering workflow
For each task, complete the design and pseudocode before coding. Record test input, predicted behaviour, actual output, metrics, boundary/failure case and interpretation. The source file `learning_lab.py` contains compact implementations that can be extended for the full experimental requirements.

## Task 1 – Diagnose and repair a poor learning protocol (5)
The supplied protocol trains and tests on the same records. This leaks training information into evaluation and usually overestimates generalisation. Other defects: no held-out test set; no validation/CV for hyperparameter choice; no explicit algorithm; accuracy alone hides minority-class failure; no baseline; no stratification or random seed; and no preprocessing leakage controls.

**Repaired pseudocode**
1. Separate features X and labels y.
2. Stratified-split once into development data and held-out test data.
3. Build a pipeline so preprocessing is fitted only inside each training fold.
4. Define explicit candidates (e.g. entropy decision tree depths 2, 4, 6, 8).
5. Select candidate using stratified k-fold CV on development data and macro-F1 (also record accuracy, precision, recall).
6. Fit majority-class baseline on development labels.
7. Refit selected model on all development data.
8. Evaluate selected model and baseline exactly once on held-out test data; report confusion matrix, accuracy, precision, recall, F1 and class support.
9. Preserve seed, split indices and all parameters.

Run the demonstration with a labelled dataset and report training score, CV score and held-out score side by side. A numeric demonstration must be generated from the actual run, not invented.

## Task 2 – Decision-tree learning (9)
**Problem model:** Inputs are attendance, assignment completion and internal marks; output is pass/fail. The objective is accurate early warning with an interpretable tree. A node tests one attribute/threshold; leaves predict a class. Candidate thresholds are midpoints between sorted observed values.

**Splitting hypothesis:** choose the feature/threshold with maximum weighted impurity reduction (information gain for entropy, or Gini decrease); stop when pure, no useful split, minimum sample count or depth limit is reached. Pseudocode is represented by recursive `fit_tree` in the source: compute parent impurity, search every feature threshold, partition rows, recursively construct left/right children, and use the majority class at leaves.

**Desk-check:** The assignment's table is to be transcribed exactly from the brief into a trace sheet. Calculate H(Y)=−Σp(c)log₂p(c), then for each candidate attribute A calculate Gain(A)=H(Y)−Σv P(v)H(Y|A=v). Show root and child calculations. The scan in the supplied document is partially broken in its table layout; verify all eight records and class labels against the original image before claiming a hand trace.

**Implementation:** The included entropy/Gini tree is implemented from scratch for numeric features. Verify against scikit-learn DecisionTreeClassifier using the same fixed split. Report accuracy, precision, recall, F1 and confusion matrix. Compare full tree with a depth/min-samples limit; record depth, leaves and train/validation/test metrics. For the challenge, change one table value, predict root change before recalculating, then test a unique identifier feature. Information gain can favour ID-like features; repair with gain ratio, minimum leaf size, pruning or feature exclusion.

## Task 3 – Hidden variables and Gaussian-mixture EM (6)
The E-step must normalise each component's joint likelihood across K for every observation: r_ik = π_k N(x_i|μ_k,σ²_k) / Σ_j π_j N(x_i|μ_j,σ²_j). Without the denominator, r_ik is not a posterior responsibility and N_k no longer means expected membership count. The M-step uses N_k=Σ_i r_ik, μ_k=Σ_i r_ik x_i/N_k, variance=Σ_i r_ik(x_i−μ_k)²/N_k and π_k=N_k/n.

The source provides repaired and deliberately faulty modes. Construct a four-or-more-point K=2 trace, plot log-likelihood and sum of weights, and run at least 20 random initialisations. For the repaired EM, log-likelihood should not decrease beyond numerical tolerance when the same model and exact EM updates are used. Include a regression case where the original expression happens to be valid (e.g. K=1).

## Task 4 – Neural-network back-propagation (9)
For layer l, z⁽ˡ⁾=W⁽ˡ⁾a⁽ˡ⁻¹⁾+b⁽ˡ⁾, a⁽ˡ⁾=g(z⁽ˡ⁾). If layer l has n_l units, z, a and δ have dimension n_l; W⁽ˡ⁾ has shape n_l × n_(l−1). For squared error, output δ⁽ᴸ⁾=(a⁽ᴸ⁾−y)⊙g'(z⁽ᴸ⁾). Hidden recurrence: δ⁽ˡ⁾=((W⁽ˡ⁺¹⁾)ᵀδ⁽ˡ⁺¹⁾)⊙g'(z⁽ˡ⁾). Errors propagate backwards because each layer's gradient depends on the next layer's error.

Mini-batch pseudocode: initialise small random weights; for each batch compute forward activations; compute loss; compute output delta; propagate deltas backwards; calculate weight/bias gradients; update parameters; stop at max epochs or validation patience. The source contains a NumPy XOR MLP demonstration. Extend it to the exact 2-2-1 desk-check parameters, numerical gradient checking, a perceptron XOR failure, and the required 8×8 digits grid of hidden units, learning rates and activations. Record loss, accuracy, macro-F1, confusion matrix and per-layer gradient norms; deliberately test a high learning rate for divergence or sigmoid saturation for vanishing gradients.

## Task 5 – Statistical, kernel and explanation-based learning (8)
**Naive Bayes:** Estimate class priors and conditional feature probabilities by counts. Laplace smoothing replaces zero probabilities with (count+α)/(class_count+α×number_of_values). Compare α=0, 0.1, 1 and 10 using accuracy, precision, recall, F1 and log-loss. The source implements categorical Naive Bayes.

**Kernel machines:** A linear separator is unsafe when the classes are non-linearly separable. SVM maximises margin; support vectors define the boundary. An RBF kernel K(x,x')=exp(−γ||x−x'||²) maps similarity into a nonlinear decision surface. Compare linear and RBF SVM with 5-fold CV over C and γ, and record support-vector count, metrics and training time. Compare with Naive Bayes and the Task 2 tree on the identical split. Use a consistent feature scaling pipeline and plot decision boundaries for two selected features.

**Explanation-based learning:** Define at least six first-order domain rules for the smart-grid hazard domain, construct an explanation tree for one labelled hazardous case, then generalise the proof into an operational rule. Test on 20 designed cases and count inference steps for direct learned-rule matching versus proving each case from the full domain theory. State that EBL compiles an explanation into a faster rule; it does not create empirical facts absent from the domain theory.

## Task 6 – Reinforcement learning energy controller (13)
**State:** occupancy, temperature/comfort bucket and electricity-price bucket (extend with time-of-day and recent trend if needed for the Markov property). **Actions:** Off, Low, High. **Reward:** negative energy cost minus a penalty for occupied discomfort. **Episode:** one simulated operating day, 15-minute slots; terminal at the end of the day.

Compare fixed thermostat, imitation, Q-learning, SARSA and model-based planning. A tabular Q-learning baseline is included. Q update: Q(s,a)←Q(s,a)+α[r+γ max_a' Q(s',a')−Q(s,a)]. Use ε-greedy exploration and discount γ. The included simulator is deliberately simple and must be calibrated/expanded to 96 quarter-hour steps and occupancy/temperature/price schedules for final evidence.

Desk-check at least four updates in a three-state/two-action toy MDP. For implementation, run at least 20 seeds, smooth reward per episode and record energy, comfort violations and convergence against a fixed-rule baseline. Attack the policy with a price spike or occupants arriving after an off period. Predict before running and explain which reward/state assumption caused the failure.

## Evidence and final submission checklist
- Design, explicit pseudocode and manual trace completed before implementation.
- Same held-out split used for all required model comparisons.
- No training-set-only performance claims.
- Metrics include confusion matrix and class-sensitive metrics where applicable.
- Fixed seeds, raw results, failure case, plots and interpretations retained.
- All numeric results in the final report regenerated from the final source.
