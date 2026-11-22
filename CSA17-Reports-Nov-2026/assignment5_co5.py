"""CSA17 CO5: drone safety, swarm frontiers, expert rules and chatbot."""
def drone_step(pos,goal,obstacles,battery):
    if battery<=1:return pos,"RETURN_OR_LAND"
    r,c=pos;gr,gc=goal
    nxt=[p for p in ((r+1,c),(r-1,c),(r,c+1),(r,c-1)) if p not in obstacles]
    if not nxt:return pos,"HOLD"
    p=min(nxt,key=lambda q:abs(q[0]-gr)+abs(q[1]-gc))
    return p,"MOVE"

def expert_diagnose(facts,rules):
    for priority,need,label,why in sorted(rules,key=lambda x:(-x[0],-len(x[1]))):
        if need<=facts:return priority,label,why
    return 0,"UNKNOWN","Insufficient evidence"

def retrieve_intent(text,intents,threshold=.35):
    words=set(text.lower().split());best=(0.0,"out_of_scope")
    for intent,phrases in intents.items():
        for phrase in phrases:
            p=set(phrase.lower().split());score=len(words&p)/max(1,len(words|p))
            if score>best[0]:best=(score,intent)
    return best if best[0]>=threshold else (best[0],"out_of_scope")

def int8_quantize(values):
    scale=max(abs(v) for v in values)/127 or 1
    return [max(-127,min(127,round(v/scale))) for v in values],scale

if __name__=="__main__":
    print("drone",drone_step((0,0),(2,2),{(0,1)},20))
    rules=[(10,{"low_pressure","motor_hot"},"pump_fault","Low pressure plus hot motor.")]
    print("expert",expert_diagnose({"low_pressure","motor_hot"},rules))
    print("intent",retrieve_intent("why flagged",{"why":["why flagged","explain alert"]}))
    print("int8",int8_quantize([.2,-.8,.4]))
