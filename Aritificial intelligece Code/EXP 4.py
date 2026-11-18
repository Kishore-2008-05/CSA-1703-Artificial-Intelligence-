from collections import deque

m=int(input("Enter number of missionaries: "))
c=int(input("Enter number of cannibals: "))

start=(m,c,0)
goal=(0,0,1)

def safe(state):
    ml,cl,b=state
    mr=m-ml
    cr=c-cl

    if ml<0 or cl<0 or ml>m or cl>c:
        return False

    if ml>0 and ml<cl:
        return False

    if mr>0 and mr<cr:
        return False

    return True


def solve():
    queue=deque([(start,[])])
    visited=[start]

    while queue:
        state,path=queue.popleft()

        if state==goal:
            print("Solution found")
            for s in path+[state]:
                print(s)
            return

        ml,cl,b=state

        if b==0:
            moves=[(1,0),(2,0),(0,1),(0,2),(1,1)]

            for x,y in moves:
                new=(ml-x,cl-y,1)

                if safe(new) and new not in visited:
                    visited.append(new)
                    queue.append((new,path+[state]))

        else:
            moves=[(1,0),(2,0),(0,1),(0,2),(1,1)]

            for x,y in moves:
                new=(ml+x,cl+y,0)

                if safe(new) and new not in visited:
                    visited.append(new)
                    queue.append((new,path+[state]))

    print("No solution")


solve()
