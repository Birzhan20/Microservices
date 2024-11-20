# Используем официальный образ Kafka
FROM confluentinc/cp-kafka:latest

# Устанавливаем рабочую директорию
WORKDIR /etc/kafka

# Копируем конфигурационный файл server.properties
COPY config/server.properties /etc/kafka/server.properties

# Устанавливаем Python и нужные зависимости
RUN apt-get update && apt-get install -y python3 python3-pip && pip3 install kafka-python

# Копируем Python скрипт для создания топиков
COPY topics.py /etc/kafka/topics.py

# Указываем путь для хранения данных Kafka
VOLUME ["/var/lib/kafka/data"]

# Запуск Kafka и Python скрипта
CMD ["sh", "-c", " \
  /etc/confluent/docker/run & \
  echo 'Waiting for Kafka to be ready...' && \
  sleep 20 && \
  kafka-server-start /etc/kafka/server.properties & \
  sleep 20 && \
  echo 'Creating Kafka topics...' && \
  python3 /etc/kafka/topics.py"]
