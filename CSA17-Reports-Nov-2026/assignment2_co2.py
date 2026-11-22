"""CSA17 CO2: UCS/Greedy/A*, alpha-beta and AC-3 demonstrations."""
import heapq, math

def grid_search(grid,start,goal,mode="astar"):
    h=lambda p:abs(p[0]-goal[0])+abs(p[1]-goal[1])
    pq=[(h(start) if mode=="greedy" else 0,start)]
    parent={start:None}; cost={start:0}; expanded=0
    while pq:
        _,u=heapq.heappop(pq); expanded+=1
        if u==goal: break
        r,c=u
        for v in ((r+1,c),(r-1,c),(r,c+1),(r,c-1)):
            if 0<=v[0]<len(grid) and 0<=v[1]<len(grid[0]) and grid[v[0]][v[1]]==0:
                ng=cost[u]+1
                if ng<cost.get(v,float("inf")):
                    cost[v]=ng; parent[v]=u
                    pr=h(v) if mode=="greedy" else ng+(h(v) if mode=="astar" else 0)
                    heapq.heappush(pq,(pr,v))
    path=None
    if goal in parent:
        path=[]; u=goal
        while u is not None: path.append(u); u=parent[u]
        path.reverse()
    return {"path":path,"cost":cost.get(goal),"expanded":expanded}

def ac3(domains,arcs):
    d={v:set(x) for v,x in domains.items()}; q=list(arcs); checks=0
    while q:
        x,y=q.pop(0); remove=set()
        for a in d[x]:
            checks+=1
            if not any(a!=b for b in d[y]): remove.add(a)
        if remove:
            d[x]-=remove
            if not d[x]: return None,checks
            q += [(z,x) for z,w in arcs if w==x and z!=y]
    return d,checks

if __name__=="__main__":
    g=[[0,0,0,0],[1,1,0,1],[0,0,0,0],[0,1,1,0]]
    for mode in ("ucs","greedy","astar"): print(mode,grid_search(g,(0,0),(3,3),mode))
    print("CSP",ac3({"A":[1,2],"B":[1,2],"C":[2,3]},[("A","B"),("B","C")]))
