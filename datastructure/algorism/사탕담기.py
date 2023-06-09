from itertools import combinations


def solution(m, weights):
    answer = 0

    for i in range(len(weights)):
        combi = combinations(weights, i)
        answer += [sum(candies) for candies in combi].count(m)

    return answer


a = 3000
b = [500, 1500, 2500, 1000, 2000]
solution(a, b)
