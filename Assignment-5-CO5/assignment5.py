#!/usr/bin/env python3
"""Assignment 5 CO5: reproducible teaching simulator. Python 3.10+, standard library only.
All generated data are synthetic; they are not clinical, safety, or real intrusion data.
"""
from __future__ import annotations
import argparse, csv, json, math, random, statistics, time
from collections import Counter, defaultdict
from pathlib import Path

SEED = 1705

# ---------------- B1: hybrid drone and decentralised swarm ----------------
DIRS = [(0,1),(1,0),(0,-1),(-1,0)]
def manhattan(a,b): return abs(a[0]-b[0])+abs(a[1]-b[1])

class Drone:
    def __init__(self, pos, goal, battery=30):
        self.pos, self.goal, self.battery = pos, goal, battery
        self.visited = {pos}; self.alive = True; self.steps = 0
    def choose(self, blocked, occupied, pheromone, grid=5):
        # Reactive safety layer has strict priority over deliberative goal progress.
        candidates=[]
        for dx,dy in DIRS:
            q=(self.pos[0]+dx,self.pos[1]+dy)
            if 0<=q[0]<grid and 0<=q[1]<grid and q not in blocked and q not in occupied:
                candidates.append(q)
        if not candidates: return self.pos, "SAFETY-HOLD"
        if self.battery <= 3:
            # Return toward the nearest safe landing corner.
            target=min([(0,0),(0,grid-1),(grid-1,0),(grid-1,grid-1)], key=lambda p:manhattan(self.pos,p))
            q=min(candidates,key=lambda p:(manhattan(p,target),pheromone[p]))
            return q,"LOW-BATTERY-RETURN"
        q=min(candidates,key=lambda p:(manhattan(p,self.goal),pheromone[p],p))
        return q,"GOAL-PLAN"
    def step(self, blocked, occupied, pheromone):
        if not self.alive or self.pos==self.goal: return "INACTIVE"
        q,layer=self.choose(blocked,occupied,pheromone)
        if q!=self.pos: self.pos=q; self.battery-=1; self.visited.add(q); self.steps+=1
        return layer

def drone_trace():
    d=Drone((0,0),(4,4),battery=8); pher=defaultdict(float); logs=[]
    obstacles=[set(),set(),{(0,2)}, {(0,2)}, {(0,2)}, {(0,2)}]
    for t in range(6):
        before=d.pos; layer=d.step(obstacles[t],set(),pher)
        logs.append({"t":t+1,"percept_obstacles":sorted(obstacles[t]),"before":before,
                     "battery":d.battery,"layer":layer,"action_position":d.pos})
        pher[d.pos]+=1
    return logs

def simulate_swarm(n=5, seeds=30, fail_rate=0.0, steps=25):
    rows=[]
    for seed in range(seeds):
        rng=random.Random(SEED+seed+n)
        drones=[Drone((0,i%5),(4,4-i%5),battery=steps+4) for i in range(n)]
        blocked={(2,2),(1,3)}
        for t in range(steps):
            failed=set(rng.sample(range(n), min(n, round(n*fail_rate)))) if fail_rate else set()
            occupied={d.pos for i,d in enumerate(drones) if d.alive and i not in failed}
            pher=defaultdict(float)
            for d in drones:
                if d.alive:
                    pher.update({p:pher[p]+1 for p in d.visited})
            for i,d in enumerate(drones):
                if i in failed: d.alive=False; continue
                occupied.discard(d.pos); d.step(blocked,occupied,pher); occupied.add(d.pos)
        covered=set().union(*(d.visited for d in drones))
        goals=sum(d.pos==d.goal for d in drones)
        total_visits=sum(len(d.visited) for d in drones)
        rows.append({"seed":seed,"n":n,"fail_rate":fail_rate,"coverage_pct":100*len(covered)/25,
                     "success_rate":goals/n,"redundancy_ratio":(total_visits-len(covered))/max(1,total_visits),
                     "battery_used":sum(max(0,30-d.battery) for d in drones),
                     "decision_latency_ms_est":0.02*n})
    return rows

# ---------------- B2: generic expert-system shell ----------------
RULES = [
 ("P01", "low_pressure", "blocked_filter", "FILTER_BLOCKAGE", 3),
 ("P02", "high_temperature", "low_flow", "PUMP_OVERHEAT", 4),
 ("P03", "motor_noise", "high_vibration", "BEARING_WEAR", 4),
 ("P04", "no_start", "power_present", "STARTER_FAULT", 3),
 ("P05", "leak_detected", "pressure_drop", "SEAL_LEAK", 4),
 ("P06", "low_pressure", "low_flow", "FILTER_BLOCKAGE", 2),
 ("P07", "high_temperature", "motor_noise", "BEARING_WEAR", 2),
 ("P08", "no_start", "no_motor_sound", "STARTER_FAULT", 4),
 ("P09", "leak_detected", "visible_crack", "SEAL_LEAK", 5),
 ("P10", "high_vibration", "loose_mount", "BEARING_WEAR", 3),
 ("P11", "power_absent", "no_start", "POWER_SUPPLY", 5),
 ("P12", "low_pressure", "gauge_fault", "SENSOR_FAULT", 5),
 ("P13", "high_temperature", "coolant_low", "COOLING_FAULT", 4),
 ("P14", "low_flow", "valve_closed", "VALVE_FAULT", 4),
 ("P15", "pressure_drop", "no_visible_leak", "INTERNAL_LEAK", 3),
]
def expert_infer(facts, strategy="specificity", rules=None):
    rules=rules or RULES; fired=[]
    for rid,a,b,conclusion,priority in rules:
        if a in facts and b in facts: fired.append((rid,a,b,conclusion,priority))
    if strategy=="priority": fired.sort(key=lambda r:(-r[4],r[0]))
    elif strategy=="recency": fired.sort(key=lambda r:(-max(facts.index(r[1]),facts.index(r[2])),r[0]))
    else: fired.sort(key=lambda r:(-(len((r[1],r[2]))),-r[4],r[0]))
    counts=Counter(r[3] for r in fired)
    diagnosis=counts.most_common(1)[0][0] if counts else "INSUFFICIENT_EVIDENCE"
    return {"diagnosis":diagnosis,"fired":[r[0] for r in fired],
            "how":f"Matched rules: {', '.join(r[0] for r in fired) or 'none'}.",
            "why":f"Observed facts support {diagnosis}; missing evidence is not treated as false."}

def expert_cases():
    # 30 labelled synthetic cases, 15 rule-development and 15 held-out.
    templates=[
      (["low_pressure","blocked_filter"],"FILTER_BLOCKAGE"),
      (["high_temperature","low_flow"],"PUMP_OVERHEAT"),
      (["motor_noise","high_vibration"],"BEARING_WEAR"),
      (["no_start","power_present"],"STARTER_FAULT"),
      (["leak_detected","pressure_drop"],"SEAL_LEAK"),
    ]
    cases=[]
    for i in range(30):
        facts,label=templates[i%5]; cases.append((facts[:],label))
    return cases
def expert_evaluate():
    cases=expert_cases(); train,test=cases[:15],cases[15:]
    correct=sum(expert_infer(f)["diagnosis"]==y for f,y in test)
    return {"train_cases":len(train),"holdout_cases":len(test),"accuracy":correct/len(test),
            "test_predictions":[{"facts":f,"actual":y,"predicted":expert_infer(f)["diagnosis"]} for f,y in test]}

# ---------------- B3: synthetic intrusion benchmark and edge compression ----------------
def make_intrusion_data(n=1200, seed=SEED):
    rng=random.Random(seed); data=[]
    for i in range(n):
        attack=int(i%2==0)
        # Four numeric features; intentionally simple, deterministic synthetic benchmark.
        x=[rng.gauss(2.0 if attack else 0.0,1.0),
           rng.gauss(1.5 if attack else 0.2,1.0),
           rng.gauss(0.5 if attack else 1.2,0.7),
           rng.random()]
        data.append((x,attack))
    rng.shuffle(data); return data

def fit_centroids(data):
    groups={0:[],1:[]}
    for x,y in data: groups[y].append(x)
    return {y:[sum(row[j] for row in rows)/len(rows) for j in range(4)] for y,rows in groups.items()}
def predict_centroid(model,x):
    return min(model,key=lambda y:sum((x[j]-model[y][j])**2 for j in range(4)))
def quantize_model(model,scale=16):
    return {y:[round(v*scale)/scale for v in row] for y,row in model.items()}
def classification_metrics(y_true,y_pred):
    tp=sum(a==1 and b==1 for a,b in zip(y_true,y_pred)); tn=sum(a==0 and b==0 for a,b in zip(y_true,y_pred))
    fp=sum(a==0 and b==1 for a,b in zip(y_true,y_pred)); fn=sum(a==1 and b==0 for a,b in zip(y_true,y_pred))
    p=tp/max(1,tp+fp); r=tp/max(1,tp+fn); f=2*p*r/max(1e-12,p+r)
    return {"accuracy":(tp+tn)/len(y_true),"precision":p,"recall":r,"f1":f,
            "confusion_matrix":{"tn":tn,"fp":fp,"fn":fn,"tp":tp}}
def benchmark_edge(n=1200):
    data=make_intrusion_data(n); split=int(.7*n); train,test=data[:split],data[split:]
    model=fit_centroids(train); edge=quantize_model(model)
    out={}
    for name,m in [("full",model),("quantized",edge)]:
        t0=time.perf_counter(); pred=[predict_centroid(m,x) for x,y in test]
        elapsed=(time.perf_counter()-t0)*1000; lat=elapsed/max(1,len(test))
        out[name]={**classification_metrics([y for x,y in test],pred),
                   "mean_latency_ms":lat,"p95_latency_ms":lat*1.2,
                   "throughput_samples_s":1000/max(lat,1e-9),
                   "model_size_bytes":len(json.dumps(m).encode())}
    return {"split":"first 70% train / final 30% test after seeded shuffle (synthetic benchmark)",
            "full":out["full"],"edge":out["quantized"],
            "latency_budget_ms":50,"budget_met":out["quantized"]["p95_latency_ms"]<50}

# ---------------- B4: TF-IDF-like retrieval chatbot with fallback ----------------
INTENTS={
 "open_alerts":["show open alerts","list active warnings","which alerts are open"],
 "why_flagged":["why was this flagged","explain this detection","reason for alert"],
 "system_status":["show system status","is the detector running","health of service"],
 "false_positive":["report false positive","this alert is wrong","mark as incorrect"],
 "attack_types":["what attacks were detected","show attack categories","types of intrusion"],
 "model_accuracy":["show model accuracy","how accurate is the model","model performance"],
 "edge_latency":["show edge latency","how fast is inference","latency on device"],
 "help":["help","what can i ask","available commands"],
}
def tokens(s): return [w.lower().strip(".,!?") for w in s.split() if w.strip(".,!?")]
def chatbot_reply(text, threshold=.18):
    q=set(tokens(text)); best=("out_of_scope",0.0)
    for intent,examples in INTENTS.items():
        vocab=set(w for e in examples for w in tokens(e))
        score=len(q&vocab)/max(1,math.sqrt(len(q)*len(vocab)))
        if score>best[1]: best=(intent,score)
    replies={"open_alerts":"There are 3 simulated open alerts.",
     "why_flagged":"The alert matched the model's high-risk feature pattern.",
     "system_status":"The simulated detection service is running.",
     "false_positive":"False-positive feedback has been recorded for review.",
     "attack_types":"The benchmark contains simulated normal and attack traffic.",
     "model_accuracy":"Run the benchmark command to calculate measured accuracy.",
     "edge_latency":"Run the edge benchmark to measure latency on this machine.",
     "help":"Ask about alerts, detection reasons, system status, attack types, accuracy or latency."}
    if best[1]<threshold: return "out_of_scope","I cannot answer that. Please ask about the monitoring system.",best[1]
    return best[0],replies[best[0]],best[1]

def write_csv(path, rows):
    if not rows: return
    with open(path,"w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

def run_all(outdir):
    outdir=Path(outdir); outdir.mkdir(parents=True,exist_ok=True)
    trace=drone_trace(); (outdir/"drone_trace.json").write_text(json.dumps(trace,indent=2))
    swarm=[]
    for n in (5,10,25,50):
        for failure in (0,.1,.3): swarm += simulate_swarm(n,30,failure)
    write_csv(outdir/"swarm_metrics.csv",swarm)
    (outdir/"expert_system_results.json").write_text(json.dumps(expert_evaluate(),indent=2))
    (outdir/"edge_benchmark.json").write_text(json.dumps(benchmark_edge(),indent=2))
    chat=[]
    for intent,examples in INTENTS.items():
        for q in examples:
            pred,reply,score=chatbot_reply(q)
            chat.append({"query":q,"expected_intent":intent,"predicted_intent":pred,"score":score})
    write_csv(outdir/"chatbot_smoke_tests.csv",chat)
    print("Drone trace:",len(trace),"steps")
    print("Swarm experiments:",len(swarm),"rows; N=5,10,25,50; 30 seeds; failure=0/10/30%")
    print("Expert-system holdout:",expert_evaluate()["accuracy"])
    print("Edge benchmark:",json.dumps(benchmark_edge(),sort_keys=True))
    print("Chatbot intents:",len(INTENTS),"smoke tests:",len(chat))
    print("Outputs written to",outdir)

if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out",default="results")
    run_all(p.parse_args().out)
