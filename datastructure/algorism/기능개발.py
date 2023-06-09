# 큐

def solution(progresses, speeds):
    deploy = []
    days = []

    for p, s in zip(progresses, speeds):
        day = ((100 - p) / s)
        days.append(int(day) + (day > int(day)))

    if len(days) > 0:
        prev = days[0]
        count = 1

        for i in range(1, len(days)):
            if prev >= days[i]:
                count += 1
            else:
                deploy.append(count)
                count = 1
                prev = days[i]

        deploy.append(count)
    return deploy


a = [93,30,55]
b = [1,30,5]
print(solution(a, b))
