"""Assignment 3 CO3: educational logic algorithms.
Run: python logic_lab.py
All domains are finite toy examples for reproducible coursework experiments.
"""
from itertools import product
from collections import defaultdict, deque

# ---------- Task 1: propositional model checking ----------
def entails(kb, query, symbols):
    """Return (entailed, models_checked, countermodels). kb/query are callables."""
    checked, countermodels = 0, []
    for bits in product([False, True], repeat=len(symbols)):
        model = dict(zip(symbols, bits))
        checked += 1
        if kb(model) and not query(model):
            countermodels.append(model)
    return not countermodels, checked, countermodels

def wumpus_kb(m):
    # Tiny 2x2 illustration: breeze at (1,1) iff pit at (1,2) or (2,1).
    return m["B11"] == (m["P12"] or m["P21"])

# ---------- Task 2/5: propositional resolution ----------
def negate(lit):
    return lit[1:] if lit.startswith("~") else "~" + lit

def resolve_pair(c1, c2):
    out = set()
    for lit in c1:
        if negate(lit) in c2:
            resolvent = (set(c1) - {lit}) | (set(c2) - {negate(lit)})
            if not any(negate(x) in resolvent for x in resolvent):
                out.add(frozenset(resolvent))
    return out

def resolution_entails(clauses, query, max_steps=10000):
    """CNF clauses as iterables of literals; refute KB AND NOT query."""
    agenda = {frozenset(c) for c in clauses}
    agenda.add(frozenset([negate(query)]))
    steps = 0
    while steps < max_steps:
        current = list(agenda)
        new = set()
        for i in range(len(current)):
            for j in range(i + 1, len(current)):
                steps += 1
                new |= resolve_pair(current[i], current[j])
                if frozenset() in new:
                    return True, steps, len(agenda)
                if steps >= max_steps:
                    break
            if steps >= max_steps:
                break
        if new.issubset(agenda) or not new:
            return False, steps, len(agenda)
        agenda |= new
    return False, steps, len(agenda)

# ---------- Task 4: first-order unification ----------
def is_var(x):
    return isinstance(x, str) and x.startswith("?")

def walk(term, subst):
    while is_var(term) and term in subst:
        term = subst[term]
    return term

def occurs(var, term, subst):
    term = walk(term, subst)
    if var == term:
        return True
    if isinstance(term, tuple):
        return any(occurs(var, t, subst) for t in term[1:])
    return False

def unify(x, y, subst=None):
    """Terms: constants/variables are strings; functions are tuples ('f', arg...)."""
    subst = {} if subst is None else dict(subst)
    x, y = walk(x, subst), walk(y, subst)
    if x == y:
        return subst
    if is_var(x):
        if occurs(x, y, subst): return None
        subst[x] = y
        return subst
    if is_var(y):
        if occurs(y, x, subst): return None
        subst[y] = x
        return subst
    if isinstance(x, tuple) and isinstance(y, tuple) and len(x) == len(y) and x[0] == y[0]:
        for a, b in zip(x[1:], y[1:]):
            subst = unify(a, b, subst)
            if subst is None: return None
        return subst
    return None

# ---------- Task 6: definite-clause inference ----------
def forward_chain(facts, rules):
    """rules: (tuple(body atoms), head atom); propositional ground demo."""
    known, firings, changed = set(facts), 0, True
    while changed:
        changed = False
        for body, head in rules:
            if set(body).issubset(known) and head not in known:
                known.add(head); firings += 1; changed = True
    return known, firings

def backward_chain(goal, facts, rules, trail=None):
    """Finite ground backward chaining with cycle detection."""
    trail = set() if trail is None else set(trail)
    if goal in facts: return True, 1
    if goal in trail: return False, 1
    trail.add(goal); expanded = 1
    for body, head in rules:
        if head == goal:
            ok = True
            for subgoal in body:
                result, count = backward_chain(subgoal, facts, rules, trail)
                expanded += count
                if not result: ok = False; break
            if ok: return True, expanded
    return False, expanded

# ---------- Task 7: medication-safety knowledge base ----------
def medication_advice(patient, drug):
    """Explainable rules. A real clinical system requires validated medical knowledge."""
    reasons = []
    if drug in patient.get("allergies", []):
        reasons.append("Drug is listed in the patient's allergies.")
    if drug in patient.get("current_medicines", []):
        reasons.append("Drug is already present in the current-medicine list; check duplication.")
    if patient.get("age", 0) < 18 and drug in {"adult_dose_A", "adult_dose_B"}:
        reasons.append("Toy rule: adult-only dose selected for a minor.")
    if patient.get("conditions", []) and drug == "contraindicated_for_condition_X" and "condition_X" in patient["conditions"]:
        reasons.append("Toy rule: drug conflicts with condition_X.")
    if reasons:
        return {"decision": "REVIEW / UNSAFE", "reasons": reasons}
    return {"decision": "NO TOY-RULE CONFLICT FOUND", "reasons": ["No encoded rule was triggered. This is not proof of clinical safety."]}

def demo():
    symbols = ["B11", "P12", "P21"]
    kb = lambda m: m["B11"] == (m["P12"] or m["P21"])
    q = lambda m: not m["P12"]  # query: square (1,2) has no pit
    print("T1 model checking:", entails(kb, q, symbols)[:2])
    print("T2 resolution (A, A=>B entails B):", resolution_entails([{"A"}, {"~A", "B"}], "B")[:2])
    print("T4 unify:", unify(("parent", "?x", "bob"), ("parent", "alice", "?y")))
    facts = {"reports_to_A_B", "reports_to_B_C"}
    rules = [(( "reports_to_A_B",), "manager_A"), (("manager_A", "reports_to_B_C"), "chain_A_C")]
    print("T6 forward:", forward_chain(facts, rules))
    print("T6 backward:", backward_chain("chain_A_C", facts, rules))
    print("T7 advisor:", medication_advice({"age": 20, "allergies": ["drug_X"]}, "drug_X"))

if __name__ == "__main__":
    demo()
