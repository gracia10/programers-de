def solution(d, budget):
    counter = 0
    for x in sorted(d):
        if budget - x < 0:
            break

        budget -= x
        counter += 1
    return counter

dd = [2, 2, 3, 3]
bb = 10
print(solution(dd, bb))
