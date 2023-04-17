def solution(brown, red):
    divisors = []
    n = brown + red

    for i in range(1, red + 1):
        if red % i == 0:
            divisors.append(i)

    while len(divisors) != 0:
        x = divisors[-1]
        y = divisors[0]

        if x * y == red and 2 * (x + y + 2) == brown:
            return [x + 2, y + 2]
        else:
            divisors.pop(0)
            divisors.pop(-1)


a = 24
b = 24
print(solution(a, b))
