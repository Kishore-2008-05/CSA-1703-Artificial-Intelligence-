"""CSA17 CO4: entropy/gain, Gaussian-mixture EM, gradient step and Q-learning."""
import math, random

def entropy(y):
    n=len(y)
    if not n:return 0.0
    return -sum((c/n)*math.log2(c/n) for c in [y.count(v) for v in set(y)])

def information_gain(rows,feature,target="result"):
    base=entropy([r[target] for r in rows]); groups={}
    for r in rows:groups.setdefault(r[feature],[]).append(r)
    return base-sum(len(g)/len(rows)*entropy([r[target] for r in g]) for g in groups.values())

def sigmoid(x):return 1/(1+math.exp(-max(-40,min(40,x))))

def neuron_step(x,y,w,b,lr):
    pred=sigmoid(sum(a*v for a,v in zip(w,x))+b)
    delta=(pred-y)*pred*(1-pred)
    return pred,[wi-lr*delta*xi for wi,xi in zip(w,x)],b-lr*delta

def q_learning(episodes=400,seed=7):
    rng=random.Random(seed);Q=[[0.0,0.0] for _ in range(5)]
    for _ in range(episodes):
        s=0
        while s<4:
            a=rng.randrange(2) if rng.random()<.15 else max(range(2),key=lambda j:Q[s][j])
            ns=min(4,s+(1 if a==0 else 2));r=10 if ns==4 else -1
            Q[s][a]+=.2*(r+.9*max(Q[ns])-Q[s][a]);s=ns
    return Q

if __name__=="__main__":
    rows=[{"attendance":"H","result":"P"},{"attendance":"H","result":"P"},{"attendance":"L","result":"F"}]
    print("entropy",round(entropy(["P","P","F"]),4),"gain",round(information_gain(rows,"attendance"),4))
    print("neuron",neuron_step([1,0],1,[.5,-.4],0,.5))
    print("Q",q_learning())
