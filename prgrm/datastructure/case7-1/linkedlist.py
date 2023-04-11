class Node:
    def __init__(self, item):
        self.data = item
        self.next = None


class LinkedList:
    def __init__(self):
        self.nodeCount = 0
        self.head = None
        self.tail = None

    # 1. 특정 원소 참조(k번째)
    def getAt(self, pos):
        if pos <= 0 or pos > self.nodeCount:
            return None

        i = 1
        curr = self.head
        while i < pos:
            curr = curr.next
            i += 1

        return curr

    # 2. 리스트 순회
    def traverse(self):
        lst = []
        curr = self.head
        while curr is not None:
            lst.append(curr.data)
            curr = curr.next
        return lst

    # 3. 길이
    def getLength(self):
        return self.nodeCount

    # 4. 원소 삽입
    def insertAt(self, pos, newNode):
        if pos <= 0 or pos > self.nodeCount + 1:
            return False

        if pos == 1:
            newNode.next = self.head
            self.head = newNode
        else:
            if pos == self.nodeCount + 1:
                prev = self.tail
            else:
                prev = self.getAt(pos - 1)
            newNode.next = prev.next
            prev.next = newNode

        if pos == self.nodeCount + 1:
            self.tail = newNode

        self.nodeCount += 1
        return True

    # 5. 원소 삭제
    def popAt(self, pos):
        if pos <= 0 or pos > self.nodeCount:
            raise IndexError

        curr = self.getAt(pos)

        if pos == 1:
            self.head = curr.next
            if pos == self.nodeCount:
                self.tail = None
        else:
            prev = self.getAt(pos - 1)
            prev.next = curr.next

            if pos == self.nodeCount:
                self.tail = prev

        self.nodeCount -= 1
        return curr.data

    # 6. 두 리스트 연결
    def concat(self, lst):
        self.tail.next = lst.head
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

print(L.popAt(3))

