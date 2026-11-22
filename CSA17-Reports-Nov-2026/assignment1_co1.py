"""CSA17 CO1: Hospital medicine-delivery robot search demonstrations."""
from collections import deque
import random, time

def make_graph(n, seed=17, degree=3):
    rng=random.Random(seed); g={i:set() for i in range(n)}
    for i in range(n-1): g[i].add(i+1); g[i+1].add(i)
    for i in range(n):
        for _ in range(degree):
            j=rng.randrange(n)
            if i!=j: g[i].add(j); g[j].add(i)
    return {k:sorted(v) for k,v in g.items()}

def reconstruct(parent, goal):
    if goal not in parent: return None
    path=[]; u=goal
    while u is not None: path.append(u); u=parent[u]
    return path[::-1]

def bfs(g,s,t):
    q=deque([s]); parent={s:None}; expanded=0; peak=1
    while q:
        peak=max(peak,len(q)); u=q.popleft(); expanded+=1
        if u==t: break
        for v in g[u]:
            if v not in parent: parent[v]=u; q.append(v)
    return {"path":reconstruct(parent,t),"expanded":expanded,"frontier_peak":peak}

def depth_limited(g,s,t,limit):
    count=0
    def visit(u,depth,path):
        nonlocal count
        count+=1
        if u==t: return path
        if depth==limit: return None
        for v in g[u]:
            if v not in path:
                ans=visit(v,depth+1,path+[v])
                if ans: return ans
        return None
    return visit(s,0,[s]),count

def iddfs(g,s,t,max_depth):
    total=0
    for d in range(max_depth+1):
        p,n=depth_limited(g,s,t,d); total+=n
        if p: return {"path":p,"expanded":total}
    return {"path":None,"expanded":total}

if __name__=="__main__":
    for n in (1000,10000,100000):
        g=make_graph(n); r=bfs(g,0,n-1)
        print("states",n,"found",r["path"] is not None,"expanded",r["expanded"],"frontier",r["frontier_peak"])
