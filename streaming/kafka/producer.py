from time import sleep
from json import dumps
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],  # 브로커 연결
    value_serializer=lambda x: dumps(x).encode('utf-8')  # 전송하려는 데이터를 json 문자열로 변환한 다음 UTF-8로 인코딩하여 직렬화하는 방법을 정의
)

for j in range(10):
    print("Iteration", j)
    data = {'counter': j}
    producer.send('topic_test', value=data)  # 토픽 이름 .. key, header 는 없
    sleep(0.5)
