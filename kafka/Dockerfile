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
RUN pip install --no-cache-dir importlib-metadata confluent-kafka

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
RUN yum -y install nc wget

# Устанавливаем OpenJDK (необходим для работы Kafka)
RUN yum -y install java-1.8.0-openjdk

# Скачиваем и устанавливаем Kafka
RUN wget https://archive.apache.org/dist/kafka/2.8.0/kafka_2.13-2.8.0.tgz && \
    tar -xvzf kafka_2.13-2.8.0.tgz && \
    mv kafka_2.13-2.8.0 /opt/kafka

# Настроим JAVA_HOME
ENV JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk
ENV PATH="${JAVA_HOME}/bin:${PATH}"

# Добавляем утилиты Kafka в PATH
ENV PATH="/opt/kafka/bin:${PATH}"

# Запускаем Kafka и затем Python-скрипт
CMD ["sh", "-c", "/etc/confluent/docker/run && kafka-server-start /etc/kafka/server.properties & while ! nc -z localhost 9092; do sleep 1; done; python3 /etc/kafka/topics.py"]
