# Используем официальный базовый образ Red Hat UBI (Universal Base Image)
FROM registry.access.redhat.com/ubi8/python-39:latest

# Устанавливаем переменные окружения для локали
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# Рабочая директория
WORKDIR /etc/kafka

# Переходим на пользователя root
USER root

# Копируем конфигурационный файл server.properties
COPY config/server.properties /etc/kafka/server.properties

# Указываем путь для хранения данных Kafka
VOLUME ["/var/lib/kafka/data"]

# Устанавливаем утилиту для проверки порта (nc) и другие зависимости
RUN yum -y install nc wget

# Скачиваем и устанавливаем Kafka
RUN wget https://archive.apache.org/dist/kafka/2.8.0/kafka_2.13-2.8.0.tgz && \
    tar -xvzf kafka_2.13-2.8.0.tgz && \
    mv kafka_2.13-2.8.0 /opt/kafka

# Запускаем Kafka и затем проверяем, доступен ли порт 9092
CMD ["sh", "-c", "/opt/kafka/bin/kafka-server-start /etc/kafka/server.properties & while ! nc -z localhost 9092; do sleep 1; done; tail -f /dev/null"]
