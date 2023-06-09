def solution(L, x):
    lower = 0
    upper = len(L) - 1

    if len(L) == 0: return -1

    while lower != upper:
        mid = int((lower + upper) / 2)

        if x > L[mid]:
            lower = mid + 1
        elif x < L[mid]:
            upper = mid - 1
        else:
            lower = mid
            break

    return lower if L[lower] == x else -1



print(solution([1,2,3,4,5,6,7,8,9,10], 6))

