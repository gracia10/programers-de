def solution(L, x):
    answer = []

    while True:
        try:
            i = L.index(x)
            answer.append(i)
            L[i] = ''
        except ValueError:
            if len(answer) == 0:
                answer = [-1]
            break

    return answer



print(solution([64, 72, 83, 72, 54], 72))