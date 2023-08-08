from kafka import KafkaConsumer
from json import loads
from time import sleep

consumer = KafkaConsumer(
    'topic_test',  # 소비할 topic
    bootstrap_servers=['localhost:9092'],  # 연결 broker
    auto_offset_reset='earliest',  # 토픽 첫번째부터 읽고싶다 <-> 최신것 부터 읽고싶다
    enable_auto_commit=True,  # 지금 읽는 offset값을 기록한다 -> 현업은 False를 두고 명시적으로 commit한다
    group_id='my-group-id',
    value_deserializer=lambda x: loads(x.decode('utf-8'))
)
for event in consumer:
    event_data = event.value
    # Do whatever you want
    print(event_data)
    sleep(2)
