from confluent_kafka import Consumer

consumer_config = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "simple_consumer_group",
    "auto.offset.reset": "earliest",
}

consumer = Consumer(consumer_config)

topic = "test"

consumer.subscribe([topic])

print(f"Консюмер подписан на топик '{topic}'")

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"Ошибка: {msg.error()}")
            continue

        print(f"Получено сообщение: {msg.value().decode('utf-8')}")

except KeyboardInterrupt:
    print("Завершение работы консюмера")

finally:
    consumer.close()
    print("Консюмер закрыт")