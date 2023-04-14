# 해시를 이용 -> 리스트 순회 O(N)
def solution(v):
    x_dict = {}
    y_dict = {}
    for x, y in v:
        x_dict[x] = x_dict.get(x, 0) + 1
        y_dict[y] = y_dict.get(y, 0) + 1

    answer = []
    answer += [k for k in x_dict if x_dict[k] == 1]
    answer += [k for k in y_dict if y_dict[k] == 1]
    return answer


a = [[1, 4], [3, 4], [3, 10]]
print(solution(a))
