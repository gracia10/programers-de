def solution(x):
    if x == 0:
        return 0
    if x == 1:
        return 1
    return solution(x-1) + solution(x-2)


print(solution(2))

