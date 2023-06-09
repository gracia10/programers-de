class MaxHeap:
    def __init__(self):
        self.data = [None]

    def insert(self, item):
        self.data.append(item)
        childIdx = len(self.data) - 1
        parentIdx = childIdx // 2
        while parentIdx != 0 and self.data[parentIdx] < self.data[childIdx]:
            self.data[parentIdx], self.data[childIdx] = self.data[childIdx], self.data[parentIdx]
            childIdx = parentIdx
            parentIdx = childIdx // 2

    def remove(self):
        if len(self.data) > 1:
            self.data[1], self.data[-1] = self.data[-1], self.data[1]
            data = self.data.pop(-1)
            self.maxHeapify(1)  # 루트 노드부터 시작
        else:
            data = None
        return data

    def maxHeapify(self, i):
        left = 2 * i
        right = 2 * i + 1
        smallest = i

        if left < len(self.data) and self.data[left] > self.data[smallest]:
            smallest = left

        if right < len(self.data) and self.data[right] > self.data[smallest]:
            smallest = right

        if smallest != i:
            self.data[smallest], self.data[i] = self.data[i], self.data[smallest]
            self.maxHeapify(smallest)


heap = MaxHeap()
heap.insert(5)
heap.insert(2)
heap.insert(10)
heap.insert(7)
heap.insert(1)

print(heap.data)