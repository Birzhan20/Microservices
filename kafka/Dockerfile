FROM confluentinc/cp-kafka:latest

# Установим рабочую директорию
WORKDIR /etc/kafka

USER root

# Установим Python Red Hat Enterprise Linux 8.10 (RHEL 8.10)
RUN dnf install -y python3 python3-pip

# Скопируем конфигурационный файл server.properties
COPY config/server.properties /etc/kafka/server.properties

# Указываем путь для хранения данных Kafka
VOLUME ["/var/lib/kafka/data"]

# Копируем Python-скрипт для работы с темами (если требуется)
COPY topics.py /etc/kafka/topics.py

# Запускаем Kafka и затем Python-скрипт
CMD ["sh", "-c", "/etc/confluent/docker/run && kafka-server-start /etc/kafka/server.properties & sleep 5 && python3 /etc/kafka/topics.py"]
