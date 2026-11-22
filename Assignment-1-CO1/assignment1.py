"""CSA17 CO1: hospital robot search experiments. Run: python assignment1.py"""
from collections import deque
from dataclasses import dataclass
import heapq,random,time,csv,json,os

@dataclass
class Result:
    algorithm:str; found:bool; path:list; cost:float; generated:int; expanded:int; max_frontier:int; seconds:float

def measured(fn):
    def run(*a,**k):
        t=time.perf_counter();r=fn(*a,**k);r.seconds=time.perf_counter()-t;return r
    return run

@measured
def bfs(g,s,goal):
    q=deque([s]);parent={s:None};gen=1;exp=0;peak=1
    while q:
        u=q.popleft();exp+=1
        if u==goal:break
        for v,_ in g.get(u,[]):
            if v not in parent:parent[v]=u;q.append(v);gen+=1
        peak=max(peak,len(q))
    found=goal in parent;p=[]
    if found:
        x=goal
        while x is not None:p.append(x);x=parent[x]
        p.reverse()
    cost=sum(next(w for v,w in g[a] if v==b) for a,b in zip(p,p[1:])) if found else float('inf')
    return Result('BFS',found,p,cost,gen,exp,peak,0)

@measured
def ucs(g,s,goal):
    pq=[(0,s)];dist={s:0};parent={s:None};gen=1;exp=0;peak=1
    while pq:
        d,u=heapq.heappop(pq)
        if d!=dist.get(u):continue
        exp+=1
        if u==goal:break
        for v,w in g.get(u,[]):
            nd=d+w
            if nd<dist.get(v,float('inf')):
                dist[v]=nd;parent[v]=u;heapq.heappush(pq,(nd,v));gen+=1
        peak=max(peak,len(pq))
    found=goal in dist;p=[]
    if found:
        x=goal
        while x is not None:p.append(x);x=parent[x]
        p.reverse()
    return Result('UCS',found,p,dist.get(goal,float('inf')),gen,exp,peak,0)

def recursive_dls(g,s,goal,limit):
    gen=1;exp=0;peak=1
    def visit(u,left,path,seen):
        nonlocal gen,exp,peak
        exp+=1;peak=max(peak,len(path))
        if u==goal:return path
        if left==0:return None
        for v,_ in g.get(u,[]):
            if v not in seen:
                gen+=1;ans=visit(v,left-1,path+[v],seen|{v})
                if ans:return ans
        return None
    t=time.perf_counter();p=visit(s,limit,[s],{s});sec=time.perf_counter()-t
    cost=sum(next(w for v,w in g[a] if v==b) for a,b in zip(p,p[1:])) if p else float('inf')
    return Result('Recursive-DLS',p is not None,p or [],cost,gen,exp,peak,sec)

def make_graph(n,seed=17):
    r=random.Random(seed);g={i:[] for i in range(n)}
    def add(a,b,w):g[a].append((b,w));g[b].append((a,w))
    for i in range(n-1):add(i,i+1,round(r.uniform(1,5),2))
    for _ in range(n//3):
        a=r.randrange(n);b=min(n-1,a+r.randint(2,max(2,min(80,n-1-a))))
        if a!=b:add(a,b,round(r.uniform(1,8),2))
    return g

def main():
    os.makedirs('results',exist_ok=True);g=make_graph(120);tests=[]
    for s,t in [(0,119),(0,120),(10,10)]:
        for fn in (bfs,ucs):
            r=fn(g,s,t);tests.append({'case':f'{s}->{t}','algorithm':r.algorithm,'found':r.found,'cost':r.cost,'depth':len(r.path)-1,'generated':r.generated,'expanded':r.expanded,'max_frontier':r.max_frontier,'seconds':r.seconds})
    small={0:[(1,1),(2,1)],1:[(0,1),(3,1)],2:[(0,1),(3,1)],3:[(1,1),(2,1)]}
    r=recursive_dls(small,0,3,3);tests.append({'case':'recursive-small','algorithm':r.algorithm,'found':r.found,'cost':r.cost,'depth':len(r.path)-1,'generated':r.generated,'expanded':r.expanded,'max_frontier':r.max_frontier,'seconds':r.seconds})
    json.dump(tests,open('results/test_cases.json','w'),indent=2)
    rows=[]
    for n in (1000,10000,100000,1000000):
        g=make_graph(n)
        for fn in (bfs,ucs):
            rs=[fn(g,0,n-1) for _ in range(5)];r=rs[-1]
            rows.append({'states':n,'algorithm':r.algorithm,'found':r.found,'cost':r.cost,'depth':len(r.path)-1,'generated_mean':sum(x.generated for x in rs)/5,'expanded_mean':sum(x.expanded for x in rs)/5,'max_frontier_max':max(x.max_frontier for x in rs),'seconds_mean_5_runs':sum(x.seconds for x in rs)/5})
    with open('results/scaling.csv','w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
    belief=[{'k':k,'belief_states_upper_bound':2**k,'plan_actions_proxy':k if sensor else k*k,'sensor':sensor} for k in (2,4,8) for sensor in (False,True)]
    json.dump(belief,open('results/belief_states.json','w'),indent=2)
    print('TESTS',json.dumps(tests,indent=2));print('SCALING',json.dumps(rows,indent=2));print('BELIEF',json.dumps(belief,indent=2))
if __name__=='__main__':main()
