class ArrayStack:

    def __init__(self):
        self.data = []

    def size(self):
        return len(self.data)

    def isEmpty(self):
        return self.size() == 0

    def push(self, item):
        self.data.append(item)

    def pop(self):
        return self.data.pop()

    def peek(self):
        return self.data[-1]


prec = {
    '*': 3, '/': 3,
    '+': 2, '-': 2,
    '(': 1
}


def solution(S):
    answer = ''
    opStack = ArrayStack()

    for c in S:
        if c in prec:

            if opStack.isEmpty() or c == '(':
                opStack.push(c)
                continue

            if prec.get(c) >= prec.get(opStack.peek()):
                opStack.push(c)
            else:
                answer += opStack.pop()
                opStack.push(c)

        elif c == ')':
            while opStack.peek() != '(':
                answer += opStack.pop()
            opStack.pop()  # '(' 제거
        else:
            answer += c

    while not opStack.isEmpty():
        answer += opStack.pop()

    return answer


print(solution("(A+B)*(C*D-E)*F/G"))

# "A+B*C/(D*E-F)+G" -> "ABC*DE*F-/+G+"