def minimax(depth, is_max):
    scores = [1000,900,8907,773,7734,88890,1234]

    if depth == 2:
        return 0

    if is_max:
        best = -999
        for s in scores:
            best = max(best, s)
        return best
    else:
        best = 999
        for s in scores:
            best = min(best, s)
        return best

print("Best score:", minimax(0, True))
