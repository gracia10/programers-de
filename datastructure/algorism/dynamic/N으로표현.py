# (1) 5읠 한번 사용해서 만들 수 있는 수 -> 5
# (2) 5을 두번 사용해서 만들 수 있는 수 -> 55, (1) +-/* (1) -> 55, 10 , 0 , 25 , 1
# (3) 5을 세번 사용해서 만들 수 있는 수 -> 555, (1) +-/* (2) , (2) +-/* (1)
# (4) 5을 네번 사용해서 만들 수 있는 수 -> 5555, (1) +-/* (3) , (2) +-/* (2) , (3) +-/* (1)
#     x를 n번 사용해서 만들 수 있는 수 -> 1 +-/* (n-1), 2 +-/* (n-2), .... ,(n-1) +-/* 1
def solution(N, number):
    answer = 0
    s = [set() for _ in range(8)]

    for i, x in enumerate(s, start=1):
        x.add(int(str(N) * i))

    for i in range(len(s)):
        for j in range(i):
            for op1 in s[j]:
                for op2 in s[i - j - 1]:
                    s[i].add(op1 + op2)
                    s[i].add(op1 - op2)
                    s[i].add(op1 * op2)
                    if op2 != 0:
                        s[i].add(op1 // op2)
        if number in s[i]:
            answer = i + 1
            break
        else:
            answer = -1
    return answer


solution(5, 12)