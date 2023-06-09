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


def solution(tokenList):
    postfixList = []
    opStack = ArrayStack()

    for token in tokenList:
        if token not in prec and token != ')':
            postfixList.append(token)
        elif token == '(':
            opStack.push(token)
        elif token == ')':
            while opStack.peek() != '(':
                postfixList.append(opStack.pop())
            opStack.pop()
        else:
            if opStack.isEmpty():
                opStack.push(token)
            elif prec.get(token) > prec.get(opStack.peek()):
                opStack.push(token)
            else:
                while not opStack.isEmpty() and prec.get(token) <= prec.get(opStack.peek()):
                    postfixList.append(opStack.pop())
                opStack.push(token)

    while not opStack.isEmpty():
        postfixList.append(opStack.pop())

    return ''.join(postfixList)

print(solution("A+B*C/(D*E-F)+G"))

# "A+B*C/(D*E-F)+G" -> "ABC*DE*F-/+G+"