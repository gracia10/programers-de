# numbers의 원소는 0 이상 1,000 이하입니다.
# 숫자를 문자열로 변환한 뒤 문자열을 이은 4글자가 큰 순서대로 정렬한다
def solution(numbers):
    numbers = [str(x) for x in numbers]
    numbers.sort(key=lambda x: (x*4)[0:4], reverse=True)

    if numbers[0] == '0':
        return '0'
    return ''.join(numbers)

a = [0,0,0,0]
print(solution(a))