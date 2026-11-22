"""CSA17 CO2: informed/online search, game trees, CSP, TSP and redesign."""
import heapq,random,math,time,csv,json,os,itertools
from collections import deque

def grid_search(grid,start,goal,mode):
    R,C=len(grid),len(grid[0]);h=lambda p:abs(p[0]-goal[0])+abs(p[1]-goal[1])
    pq=[(0,0,start)];dist={start:0};parent={};gen=1;exp=0;peak=1
    while pq:
        _,g,u=heapq.heappop(pq)
        if mode!='greedy' and g!=dist.get(u):continue
        exp+=1
        if u==goal:break
        for dr,dc in ((1,0),(-1,0),(0,1),(0,-1)):
            v=(u[0]+dr,u[1]+dc)
            if 0<=v[0]<R and 0<=v[1]<C and not grid[v[0]][v[1]]:
                ng=g+1
                if mode=='greedy':
                    if v in parent or v==start:continue
                    parent[v]=u;heapq.heappush(pq,(h(v),ng,v));gen+=1
                elif ng<dist.get(v,float('inf')):
                    dist[v]=ng;parent[v]=u;heapq.heappush(pq,(ng if mode=='ucs' else ng+h(v),ng,v));gen+=1
        peak=max(peak,len(pq))
    found=goal==start or goal in parent;path=[]
    if found:
        x=goal;path=[x]
        while x!=start:x=parent[x];path.append(x)
        path.reverse()
    optimal_cost=None
    if found:
        q=deque([(start,0)]);seen={start}
        while q:
            p,d=q.popleft()
            if p==goal:optimal_cost=d;break
            for dr,dc in ((1,0),(-1,0),(0,1),(0,-1)):
                z=(p[0]+dr,p[1]+dc)
                if 0<=z[0]<R and 0<=z[1]<C and not grid[z[0]][z[1]] and z not in seen:seen.add(z);q.append((z,d+1))
    return {'algorithm':mode,'found':found,'path_cost':len(path)-1 if found else None,'optimal':not found or len(path)-1==optimal_cost,'generated':gen,'expanded':exp,'max_frontier':peak,'path':path}

def make_grid(kind):
    R=C=25;g=[[False]*C for _ in range(R)]
    if kind=='cluttered':
        for r in range(R):
            for c in range(C):
                if (r*7+c*11)%13<3 and (r,c) not in ((0,0),(24,24)):g[r][c]=True
    elif kind=='maze':
        for c in range(2,C-1,3):
            for r in range(R):
                if r%6!=((c//3)%6):g[r][c]=True
    elif kind=='trap':
        for r in range(1,R-1):g[r][12]=True
        g[23][12]=False
    return g

def online_dfs(rows=8,cols=8,target=(7,7),seed=4,density=.16):
    rng=random.Random(seed);blocked={(r,c) for r in range(rows) for c in range(cols) if rng.random()<density};blocked.discard((0,0));blocked.discard(target)
    def neigh(p):
        r,c=p
        return [(r+dr,c+dc) for dr,dc in ((0,1),(1,0),(0,-1),(-1,0)) if 0<=r+dr<rows and 0<=c+dc<cols and (r+dr,c+dc) not in blocked]
    q=deque([((0,0),0)]);seen={(0,0)};optimal=None
    while q:
        p,d=q.popleft()
        if p==target:optimal=d;break
        for z in neigh(p):
            if z not in seen:seen.add(z);q.append((z,d+1))
    moves=0;revisits=0;visited={(0,0)};stack=[((0,0),iter(neigh((0,0))))]
    while stack:
        u,it=stack[-1]
        if u==target:return {'found':True,'moves':moves,'revisited':revisits,'optimal_cost':optimal,'competitive_ratio':moves/max(1,optimal or 1)}
        v=next(it,None)
        if v is None:
            stack.pop()
            if stack:moves+=1;revisits+=1
        elif v not in visited:
            visited.add(v);moves+=1;stack.append((v,iter(neigh(v))))
    return {'found':False,'moves':moves,'revisited':revisits,'optimal_cost':optimal,'competitive_ratio':None}

def evaluation_function(position):
    """Student-defined leaf evaluation: material + mobility + objective progress."""
    if isinstance(position,(int,float)): return float(position)
    return 3*position.get('material',0)+position.get('mobility',0)+2*position.get('objective_progress',0)-2*position.get('danger',0)

def depth_limited_minimax(tree,depth,maximizing=True):
    """Depth-limited minimax; evaluate positions at the cutoff depth."""
    calls=0
    def visit(node,left,maxing):
        nonlocal calls
        if left==0 or not isinstance(node,list):
            calls+=1
            return evaluation_function(node)
        values=[visit(ch,left-1,not maxing) for ch in node]
        return max(values) if maxing else min(values)
    value=visit(tree,depth,maximizing)
    return value,calls

def minimax(tree,depth,maximizing=True):
    if not isinstance(tree,list):return tree,1,0
    vals=[];nodes=1
    for ch in tree:
        v,n,_=minimax(ch,depth-1,not maximizing);vals.append(v);nodes+=n
    return (max(vals) if maximizing else min(vals)),nodes,0

def alphabeta(tree,alpha=-math.inf,beta=math.inf,maximizing=True):
    if not isinstance(tree,list):return tree,1,0
    nodes=1;cuts=0;best=-math.inf if maximizing else math.inf
    for i,ch in enumerate(tree):
        v,n,c=alphabeta(ch,alpha,beta,not maximizing);nodes+=n;cuts+=c
        if maximizing:best=max(best,v);alpha=max(alpha,best)
        else:best=min(best,v);beta=min(beta,best)
        if beta<=alpha:cuts+=len(tree)-i-1;break
    return best,nodes,cuts

def exam_csp(domains,edges,propagate=True):
    D={v:set(x) for v,x in domains.items()};checks=nodes=backs=0
    def revise(x,y):
        nonlocal checks
        remove=set()
        for a in D[x]:
            support=False
            for b in D[y]:
                checks+=1
                if a!=b:support=True;break
            if not support:remove.add(a)
        if remove:D[x]-=remove;return True
        return False
    def ac3(queue):
        while queue:
            x,y=queue.pop(0)
            if revise(x,y):
                if not D[x]:return False
                for z,w in edges:
                    if w==x and z!=y:queue.append((z,x))
                    if z==x and w!=y:queue.append((w,x))
        return True
    def backtrack():
        nonlocal nodes,backs
        if all(len(d)==1 for d in D.values()):return {v:next(iter(d)) for v,d in D.items()}
        v=min((x for x in D if len(D[x])>1),key=lambda x:len(D[x]));snapshot={x:set(d) for x,d in D.items()}
        for val in sorted(D[v]):
            nodes+=1;D[v]={val};ok=True
            for a,b in edges:
                if a==v and len(D[b])==1 and val in D[b]:ok=False
                if b==v and len(D[a])==1 and val in D[a]:ok=False
            if ok and (not propagate or ac3([(a,b) for a,b in edges]+[(b,a) for a,b in edges])):
                ans=backtrack()
                if ans:return ans
            D.clear();D.update({x:set(d) for x,d in snapshot.items()});backs+=1
        return None
    if propagate and not ac3([(a,b) for a,b in edges]+[(b,a) for a,b in edges]):return {'solution':None,'nodes':nodes,'backtracks':backs,'checks':checks,'domains':{k:sorted(v) for k,v in D.items()}}
    sol=backtrack()
    return {'solution':sol,'nodes':nodes,'backtracks':backs,'checks':checks,'domains':{k:sorted(v) for k,v in D.items()}}

def tour_cost(tour,dist):return sum(dist[tour[i]][tour[(i+1)%len(tour)]] for i in range(len(tour)))
def exhaustive_tsp(dist):
    n=len(dist);best=float('inf');besttour=None;count=0
    for p in itertools.permutations(range(1,n)):
        t=(0,)+p;c=tour_cost(t,dist);count+=1
        if c<best:best,besttour=c,t
    return best,besttour,count

def two_opt(dist,restarts=20,seed=3):
    rng=random.Random(seed);n=len(dist);best=float('inf');besttour=None
    for _ in range(restarts):
        t=[0]+rng.sample(list(range(1,n)),n-1);improved=True
        while improved:
            improved=False;cur=tour_cost(t,dist)
            for i in range(1,n-1):
                for j in range(i+1,n):
                    cand=t[:i]+list(reversed(t[i:j+1]))+t[j+1:];c=tour_cost(cand,dist)
                    if c<cur:t=cand;cur=c;improved=True;break
                if improved:break
        c=tour_cost(t,dist)
        if c<best:best,besttour=c,t[:]
    return best,besttour

def main():
    os.makedirs('results',exist_ok=True);results={}
    gridrows=[]
    for name in ('open','cluttered','maze','trap'):
        g=make_grid(name)
        for alg in ('ucs','greedy','astar'):
            t=time.perf_counter();r=grid_search(g,(0,0),(24,24),alg);r['seconds']=time.perf_counter()-t;r['map']=name;gridrows.append(r)
    results['grid_search']=gridrows
    results['online_dfs']=[online_dfs(8,8,(7,7),s) for s in (0,1,2,7)]
    # Vary map dimensions, target distance and dead-end/obstacle density.
    results['online_matrix']=[]
    for size in (6,8,12):
        for density in (.05,.16,.30):
            for target in ((size//2,size//2),(size-1,size-1)):
                for seed in (11,12,13):
                    row=online_dfs(size,size,target,seed,density)
                    results['online_matrix'].append({'size':size,'density':density,'target':target,'seed':seed,**row})
    good=[[8,9],[1,2]];bad=[[1,2],[8,9]];equal=[[4,4],[4,4]]
    results['game_trees']={n:{'minimax':minimax(t,3),'alphabeta':alphabeta(t)} for n,t in [('favorable',good),('unfavorable',bad),('equal',equal)]}
    results['minimax_scaling']=[{'branching':b,'depth':d,'nodes':sum(b**i for i in range(d+1)),'leaf_evaluations':b**d} for b,d in ((2,3),(3,4),(4,5))]
    results['depth_limited_evaluation_demo']={'value_and_evaluation_calls':depth_limited_minimax([[3,5],[1,9]],2)}
    domains={'A':[1,2],'B':[1,2],'C':[1,2],'D':[1,2]};edges=[('A','B'),('B','C'),('C','D'),('D','A')]
    impossible={'P':[1],'Q':[1],'R':[1,2]};iedges=[('P','Q')]
    results['csp']={'without_propagation':exam_csp(domains,edges,False),'with_propagation':exam_csp(domains,edges,True),'propagation_failure_without_search':exam_csp(impossible,iedges,True)}
    tsp=[]
    for n in (6,7,8):
        pts=[(math.cos(2*math.pi*i/n),math.sin(2*math.pi*i/n)) for i in range(n)];dist=[[math.dist(a,b) for b in pts] for a in pts]
        opt,ot,count=exhaustive_tsp(dist);runs=[]
        for seed in range(20):
            val,t=two_opt(dist,1,seed);runs.append({'cost':val,'gap_percent':100*(val-opt)/opt})
        tsp.append({'n':n,'permutations':count,'optimum':opt,'optimal_tour':ot,'local_runs':runs,'mean_gap_percent':sum(x['gap_percent'] for x in runs)/20})
    results['tsp']=tsp
    tree=[[[3,5],[6,9]],[[1,2],[0,4]],[[7,8],[2,3]]];original=alphabeta(tree)
    def last_leaf(node):
        while isinstance(node,list): node=node[-1]
        return node
    def ordered(node,maxing=True):
        if not isinstance(node,list):return node
        scored=[(last_leaf(ch),ch) for ch in node];scored.sort(key=lambda x:x[0],reverse=maxing)
        return [ordered(ch,not maxing) for _,ch in scored]
    results['redesign']={'baseline_value_nodes_cutoffs':original,'ordered_value_nodes_cutoffs':alphabeta(ordered(tree)),'design':'order children by inexpensive estimate before alpha-beta; ordering has overhead'}
    json.dump(results,open('results/experiments.json','w'),indent=2)
    with open('results/grid_search.csv','w',newline='') as f:
        rows=[{k:v for k,v in x.items() if k!='path'} for x in gridrows];w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
    print(json.dumps(results,indent=2))
if __name__=='__main__':main()
