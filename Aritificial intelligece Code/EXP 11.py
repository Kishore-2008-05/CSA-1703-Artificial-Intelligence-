colors = ['Red', 'Green', 'Blue']

graph = {
    'A': ['B', 'C'],
    'B': ['A', 'C', 'D'],
    'C': ['A', 'B', 'D'],
    'D': ['B', 'C']
}

assigned = {}

def solve(regions):
    if not regions:
        return True

    r = regions[0]

    for c in colors:
        if all(assigned.get(n) != c for n in graph[r]):
            assigned[r] = c

            if solve(regions[1:]):
                return True

            del assigned[r]

    return False

if solve(list(graph)):
    for r, c in assigned.items():
        print(r, ":", c)
else:
    print("No solution")
