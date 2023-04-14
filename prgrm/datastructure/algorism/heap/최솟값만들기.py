# A는 정렬 후 최소값 , B는 정렬 후 최대값 가져와 연산
# a) 최소힙, 최대힙 을 사용한 경우 -> 힙변환 O(N) , n번 값반환 O(NlogN) ->
import heapq
import time


def solution1(A, B):
    answer = 0
    B = [-x for x in B]

    heapq.heapify(A)
    heapq.heapify(B)

    while len(A) > 0:
        answer += heapq.heappop(A) * (-heapq.heappop(B))

    return answer


# b) 선형 배열을 사용한 경우 -> 정렬 O(NlogN), n번 값반환 O(N^2) => 효율성 30.4
def solution2(A, B):
    answer = 0

    A.sort()
    B.sort(reverse=True)

    for i in range(len(A)):
        answer += A.pop(-1) * B.pop(-1)

    return answer


a = [i for i in range(1000)]
b = [i for i in range(1000)]

start_time = time.time()
solution1(a, b)
end_time = time.time()
print("elapsed time:", end_time - start_time)  # 0.0006988048553466797

start_time = time.time()
solution2(a, b)
end_time = time.time()
print("elapsed time:", end_time - start_time)  # 7.867813110351562e-06
