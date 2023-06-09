class Node:
    def __init__(self, item):
        self.data = item
        self.next = None


class LinkedList:
    def __init__(self):
        self.nodeCount = 0
        self.head = Node(None)
        self.tail = None
        self.head.next = self.tail

    # 1. 특정 원소 참조(k번째)
    def getAt(self, pos):
        if pos < 0 or pos > self.nodeCount:
            return None

        i = 0
        curr = self.head
        while i < pos:
            curr = curr.next
            i += 1

        return curr

    # 2. 리스트 순회
    def traverse(self):
        lst = []
        curr = self.head
        while curr.next:
            curr = curr.next
            lst.append(curr.data)
        return lst

    # 3. 길이
    def getLength(self):
        return self.nodeCount

    # 4-1. 원소 삽입
    def insertAfter(self, prev, newNode):
        newNode.next = prev.next
        if prev.next is None:
            self.tail = newNode
        prev.next = newNode

        self.nodeCount += 1
        return True

    # 4-2. 원소 삽입 (head를 체크할 필요가 없다)
    def insertAt(self, pos, newNode):
        if pos <= 0 or pos > self.nodeCount + 1:
            return False

        if pos != 1 and pos == self.nodeCount + 1:
            prev = self.tail
        else:
            prev = self.getAt(pos - 1)

        return self.insertAfter(prev, newNode)

    # 5-1. 원소 삭제
    def popAfter(self, prev):
        if prev.next is None:
            return None

        curr = prev.next
        if curr.next is None:
            self.tail = prev
        prev.next = curr.next
        self.nodeCount -= 1
        return curr.data

    # 5-2. 원소 삭제
    def popAt(self, pos):
        if pos <= 0 or pos > self.nodeCount:
            raise IndexError

        prev = self.getAt(pos - 1)
        return self.popAfter(prev)

    # 6. 두 리스트 연결
    def concat(self, lst):
        self.tail.next = lst.head.next
        if lst.tail:
            self.tail = lst.tail
        self.nodeCount += lst.nodeCount


a = Node(67)
b = Node(34)
c = Node(28)
L = LinkedList()

L.insertAt(1, a)
L.insertAt(1, b)
L.insertAt(1, c)

# print(L.popAt(3))

