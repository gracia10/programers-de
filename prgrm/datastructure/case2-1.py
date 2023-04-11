def solution(L, x):
    for i, n in enumerate(L):
        if n >= x:
            L.insert(i, x)
            break

        if i+1 == len(L):
            L.append(x)
            break

    return L


solution([1, 1, 1], 65)
