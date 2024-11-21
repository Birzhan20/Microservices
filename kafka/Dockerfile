# Используем официальный базовый образ Red Hat UBI (Universal Base Image)
FROM registry.access.redhat.com/ubi8/python-39:latest

# Устанавливаем переменные окружения для локали
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# Рабочая директория
WORKDIR /etc/kafka

# Переходим на пользователя root
USER root

# Обновляем pip и устанавливаем необходимые зависимости
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir importlib-metadata confluent-docker-utils

# Устанавливаем все зависимости из requirements.txt
COPY requirements.txt /etc/kafka/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /etc/kafka/requirements.txt

# Копируем конфигурационный файл server.properties
COPY config/server.properties /etc/kafka/server.properties

# Указываем путь для хранения данных Kafka
VOLUME ["/var/lib/kafka/data"]

# Копируем Python-скрипт для работы с темами
COPY topics.py /etc/kafka/topics.py

# Устанавливаем утилиту для проверки порта (nc) и другие зависимости
RUN yum -y install nc

# Запускаем Kafka и затем Python-скрипт
CMD ["sh", "-c", "/etc/confluent/docker/run && kafka-server-start /etc/kafka/server.properties & while ! nc -z localhost 9092; do sleep 1; done; python3 /etc/kafka/topics.py"]
