import uuid
from typing import List

from faker import Faker

from streaming.kafka.fake_person.person import Person
from kafka import KafkaAdminClient, KafkaProducer
from kafka.admin import NewTopic
from kafka.errors import TopicAlreadyExistsError


def create_topic(bootstrap_servers, name, partitions, replica=1):
    client = KafkaAdminClient(bootstrap_servers=bootstrap_servers)
    try:
        topic = NewTopic(
            name=name,
            num_partitions=partitions,
            replication_factor=replica
        )
        client.create_topics([topic])
    except TopicAlreadyExistsError as e:
        print(e)
        pass
    finally:
        client.close()


def main():
    # create a topic first
    topic_name = "fake_people"
    bootstrap_servers = ["localhost:9092"]
    create_topic(bootstrap_servers, topic_name, 4)

    # ingest some random people events
    people: List[Person] = []
    faker = Faker()
    producer = KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        client_id="Fake_Person_Producer",
    )

    for i in range(100):
        person = Person(id=str(uuid.uuid4()), name=faker.name(), title=faker.job().title())
        print(f"{i} ::: ID: {person.id}, Name: {person.name}, Title: {person.title}")

        people.append(person)
        producer.send(
            topic=topic_name,
            key=person.title.lower().replace(r's+', '-').encode('utf-8'),
            value=person.json().encode('utf-8'))

    producer.flush()


if __name__ == '__main__':
    main()
