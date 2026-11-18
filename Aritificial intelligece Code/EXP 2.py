n=int(input("enter the number: "))
board=[-1]*n

def safe(r,c):
    for i in range(r):
        if board[i] == c or abs(board[i]-c) == abs(i-r):
            return False
    return True

def solve(r):
    if r == n:
        return True

    for c in range(n):
        if safe(r,c):
            board[r] = c

            if solve(r+1):
                return True

            board[r] = -1

    return False


if solve(0):
    for i in range(n):
        print(" ".join("Q" if board[i] == c else "." for c in range(n)))
else:
    print("no solution")
