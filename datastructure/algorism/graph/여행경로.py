# dict를 활용한다 ICN -> {[ATL,SFO]}
# 역순으로 정렬 한다 ICN -> {[SFO, ATL]}

# 현재 공항 정보를 Stack에 넣는다
# 다음 공항 중 알파벳이 작은 것 1개를 Stack에 넣는다
# - 공항의 다음 경로가 없으면 Stack에서 빼 별도로 저장한다
# 인천 공항에서 갈 수 있는 경로가 없는 경우 Stack에서 꺼낸다 (*역순이다)
def solution(tickets):
    routes = {}
    for t in tickets:
        routes[t[0]] = routes.get(t[0], []) + [t[1]]
    for r in routes:
        routes[r].sort(reverse=True)

    stack = ["ICN"]
    path = []

    while len(stack) > 0:
        top = stack[-1]
        # 공항에서 출발하는 표가 한개도 없는 경우, 있었는데 다 쓴 경우
        if top not in routes or len(routes[top]) == 0:
            path.append(stack.pop())
        else:
            stack.append(routes[top].pop())
    return path[::-1]


a = [["ICN", "SFO"], ["ICN", "ATL"], ["SFO", "ATL"], ["ATL", "ICN"], ["ATL","SFO"]]
solution(a)