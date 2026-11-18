import heapq

def astar(graph, h, start, goal):
    pq = [(h[start], 0, start, [start])]
    visited = set()

    while pq:
        f, g, node, path = heapq.heappop(pq)

        if node == goal:
            return path, g

        if node in visited:
            continue
        visited.add(node)

        for neighbor, cost in graph[node]:
            if neighbor not in visited:
                ng = g + cost
                heapq.heappush(pq, (ng + h[neighbor], ng,
                                    neighbor, path + [neighbor]))
    return None

# Graph: neighbor and edge cost
graph = {
    'A': [('B', 1), ('C', 4)],
    'B': [('D', 2), ('E', 5)],
    'C': [('E', 1)],
    'D': [('E', 1)],
    'E': []
}

# Heuristic values
h = {'A': 4, 'B': 3, 'C': 2, 'D': 1, 'E': 0}

print(astar(graph, h, 'A', 'E'))
