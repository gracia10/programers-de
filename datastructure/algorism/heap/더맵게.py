# 스코빌 배열의 길이는 꽤길다 - 1,000,000
# 배열의 최솟값을 꺼내고 연산결과를 삽입하면 복잡도가 높다 -> O(n^2)
# heap 을 쓰면 최소/최대 값 삽입, 삭제가 효율적이다 -> O(logn)
import heapq

def solution(scoville, K):
    answer = 0

    heapq.heapify(scoville)

    while True:
        min1 = heapq.heappop(scoville)
        if min1 >= K:
            break
        elif len(scoville) == 0:
            answer = -1
            break
        min2 = heapq.heappop(scoville)
        new_scoville = min1 + (min2 * 2)
        heapq.heappush(scoville, new_scoville)
        answer += 1
    return answer