def solution(x):
    if x == 0:
        return 0
    elif x == 1:
        return 1
    else:
        current = 0
        p1 = 1
        p2 = 0
        for i in range(2, x+1):
            current = p1 + p2
            p2 = p1
            p1 = current
    return current

print(solution(2))
