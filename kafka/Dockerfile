FROM confluentinc/cp-kafka:latest

WORKDIR /etc/kafka

USER root

# Установим необходимые зависимости Python
RUN pip install --no-cache-dir --upgrade requests kafka-python

# Копируем конфигурационный файл server.properties
COPY config/server.properties /etc/kafka/server.properties

# Указываем путь для хранения данных Kafka
VOLUME ["/var/lib/kafka/data"]

# Копируем Python-скрипт для работы с темами
COPY topics.py /etc/kafka/topics.py

# Запускаем Kafka и затем Python-скрипт
CMD ["sh", "-c", "/etc/confluent/docker/run && kafka-server-start /etc/kafka/server.properties & while ! nc -z localhost 9092; do sleep 1; done; python3 /etc/kafka/topics.py"]
