# 선형배열 시간 복잡도 O(N)
def solution(max_weight, specs, names):
    specs = {x: int(y) for x, y in specs}

    truck = 1
    curr_weight = 0
    for x in names:
        if curr_weight + specs[x] > max_weight:
            truck += 1
            curr_weight = specs[x]
        else:
            curr_weight += specs[x]

    return truck


def solution_reverse(max_weight, specs, names):
    specs = {x: int(y) for x, y in specs}

    truck = 1
    curr_weight = max_weight
    for x in names:
        if curr_weight >= specs[x]:
            curr_weight -= specs[x]
        else:
            truck += 1
            curr_weight = max_weight - specs[x]

    return truck


a = 13
b = [["toy", "13"], ["snack", "13"]]
c = ["toy", "snack", "toy"]
print(solution_reverse(a, b, c))
