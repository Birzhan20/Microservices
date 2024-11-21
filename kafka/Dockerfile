FROM confluentinc/cp-kafka:latest

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

WORKDIR /etc/kafka

USER root

# Убедимся, что pip обновлен
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir importlib-metadata confluent-docker-utils==0.0.82

# Установим все необходимые зависимости из requirements.txt
COPY requirements.txt /etc/kafka/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /etc/kafka/requirements.txt

# Копируем конфигурационный файл server.properties
COPY config/server.properties /etc/kafka/server.properties

# Указываем путь для хранения данных Kafka
VOLUME ["/var/lib/kafka/data"]

# Копируем Python-скрипт для работы с темами
COPY topics.py /etc/kafka/topics.py

# Запускаем Kafka и затем Python-скрипт
CMD ["sh", "-c", "/etc/confluent/docker/run && kafka-server-start /etc/kafka/server.properties & while ! nc -z localhost 9092; do sleep 1; done; python3 /etc/kafka/topics.py"]