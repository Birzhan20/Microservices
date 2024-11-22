# -*- coding: utf-8 -*-
from kafka import KafkaAdminClient
from kafka.admin import NewTopic
import time
import socket


topics_list = [
    "category-index", "category-seo", "goods-category-result", "goods-index", "goods-seo",
    "d-a-categories-index", "d-a-categories-seo", "d-a-goods-index", "d-a-goods-seo", "d-a-result",
    "d-g-categories-index", "d-g-categories-seo", "d-g-goods-index", "d-g-goods-seo", "d-g-result",
    "d-r-categories-index", "d-r-categories-seo", "d-r-goods-index", "d-r-goods-seo", "d-r-result",
    "d-s-categories-index", "d-s-categories-seo", "d-s-result", "d-s-services-index", "d-s-services-seo",
    "jud-index", "jud-seo", "phys-index", "phys-jud-result", "phys-seo",
    "vacancy-index", "vacancy-seo", "vacancy-resume-index", "vacancy-resume-seo", "vacancy-result",
    "translation", "translation-res",
]


def create_topics(bootstrap_servers, topics):
    admin_client = KafkaAdminClient(bootstrap_servers=bootstrap_servers)

    new_topics = [NewTopic(name=topic, num_partitions=3, replication_factor=2) for topic in topics]

    try:
        admin_client.create_topics(new_topics=new_topics, validate_only=False)
        print("Topics created successfully.")
    except Exception as e:
        print(f"Error creating topics: {e}")
    finally:
        admin_client.close()


def wait_for_kafka(bootstrap_servers, retries=30, delay=10):
    """Функция для ожидания доступности Kafka"""
    host, port = bootstrap_servers.split(":")
    for _ in range(retries):
        try:
            sock = socket.create_connection((host, int(port)), timeout=1)
            sock.close()
            print(f"Kafka is up and running at {bootstrap_servers}")
            return True
        except (socket.timeout, socket.error):
            print(f"Waiting for Kafka to be available at {bootstrap_servers}...")
            time.sleep(delay)
    return False


if __name__ == "__main__":
    kafka_address = 'kafka:9092'  # Используйте правильное имя сервиса или IP-адрес

    # Ожидаем, пока Kafka не станет доступной
    if wait_for_kafka(kafka_address):
        create_topics(kafka_address, topics_list)
        print("Topics created")
    else:
        print(f"Failed to connect to Kafka at {kafka_address}")
