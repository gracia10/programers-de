class Node:
    def __init__(self, item):
        self.data = item
        self.prev = None
        self.next = None


class DoublyLinkedList:
    def __init__(self):
        self.nodeCount = 0
        self.head = Node(None)
        self.tail = Node(None)
        self.head.prev = None
        self.head.next = self.tail
        self.tail.prev = self.head
        self.tail.next = None

    # 1. 특정 원소 참조(k번째)
    def getAt(self, pos):
        if pos < 0 or pos > self.nodeCount:
            return None

        if pos > self.nodeCount // 2:
            i = 0
            curr = self.tail
            while i < self.nodeCount - pos + 1:
                curr = curr.prev
                i += 1
        else:
            i = 0
            curr = self.head
            while i < pos:
                curr = curr.next
                i += 1

        return curr

    # 2-1. 리스트 정순회
    def traverse(self):
        lst = []
        curr = self.head
        while curr.next.next:
            curr = curr.next
            lst.append(curr.data)
        return lst

    # 2-2. 리스트 역순회
    def reverse(self):
        lst = []
        curr = self.tail
        while curr.prev.prev:
            curr = curr.prev
            lst.append(curr.data)
        return lst

    # 3. 길이
    def getLength(self):
        return self.nodeCount

    # 4-1. 원소 앞에 삽입
    def insertAfter(self, prev, newNode):
        next = prev.next
        newNode.prev = prev
        newNode.next = next
        prev.next = newNode
        next.prev = newNode
        self.nodeCount += 1
        return True

    # 4-2. 원소 뒤에 삽입
    def insertBefore(self, next, newNode):
        prev = next.prev
        newNode.next = next
        newNode.prev = prev
        prev.next = newNode
        next.prev = newNode
        self.nodeCount += 1
        return True

    # 4-3. 원소 삽입
    def insertAt(self, pos, newNode):
        if pos <= 0 or pos > self.nodeCount + 1:
            return False

        prev = self.getAt(pos - 1)
        return self.insertAfter(prev, newNode)

    # 5-1. 원소 앞 삭제
    def popAfter(self, prev):
        curr = prev.next
        prev.next = curr.next
        curr.next.prev = prev
        self.nodeCount -= 1
        return curr.data

    # 5-2. 원소 뒤 삭제
    def popBefore(self, next):
        curr = next.prev
        next.prev = curr.prev
        curr.prev.next = next
        self.nodeCount -= 1
        return curr.data

    # 5-3. 원소 삭제
    def popAt(self, pos):
        if pos <= 0 or pos > self.nodeCount:
            raise IndexError

        prev = self.getAt(pos - 1)
        return self.popAfter(prev)

    # 6. 두 리스트 연결
    def concat(self, lst):
        if lst.head.next != lst.tail:
            self.tail.prev.next = lst.head.next
            lst.head.next.prev = self.tail.prev
            self.tail = lst.tail
            self.nodeCount += lst.nodeCount


a = Node(1)
b = Node(2)
c = Node(3)
L1 = DoublyLinkedList()
L2 = DoublyLinkedList()

L1.insertAt(1, a)
L1.insertAt(2, b)
L1.insertAt(3, c)
L2.insertAt(1, Node(4))

print(L1.concat(L2))

