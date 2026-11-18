graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': [],
    'F': []
}

visited = []

def dfs(node):
    visited.append(node)

    for neighbour in graph[node]:
        if neighbour not in visited:
            dfs(neighbour)

dfs('A')
print("DFS Traversal:", visited)
