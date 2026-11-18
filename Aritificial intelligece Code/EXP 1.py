
def h(a, goal):
    x = 0
    for i in range(9):
        if a[i] != 0:
            p = goal.index(a[i])
            x += abs(i // 3 - p // 3) + abs(i % 3 - p % 3)
    return x


def puzzle(start, goal):
    states = [(h(start, goal), 0, start, [])]
    visited = []

    while states:
        states.sort()
        f, g, a, path = states.pop(0)

        if a in visited:
            continue

        visited.append(a)

        if a == goal:
            print("Puzzle solved")
            print("Moves:", g)

            for state in path + [a]:
                print(state[:3])
                print(state[3:6])
                print(state[6:])
                print()

            return

        z = a.index(0)

        for n in [z-3, z+3, z-1, z+1]:
            if 0 <= n < 9 and (
                n == z-3 or
                n == z+3 or
                (n == z-1 and z % 3 != 0) or
                (n == z+1 and z % 3 != 2)
            ):
                b = a[:]
                b[z], b[n] = b[n], b[z]

                if b not in visited:
                    if b not in [item[2] for item in states]:
                        states.append(
                            (g+1+h(b, goal), g+1, b, path+[a])
                        )


start = list(map(int, input("Enter the nine numbers: ").split()))
goal = [1, 2, 3, 4, 5, 6, 7, 8, 0]

puzzle(start, goal)
