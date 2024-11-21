# kafka/Dockerfile
FROM confluentinc/cp-kafka:latest

# Установим рабочую директорию
WORKDIR /etc/kafka

# Скопируем конфигурационный файл server.properties
COPY config/server.properties /etc/kafka/server.properties

# Указываем путь для хранения данных Kafka
VOLUME ["/var/lib/kafka/data"]

# Запускаем Kafka с использованием кастомного конфигурационного файла
CMD ["sh", "-c", "/etc/confluent/docker/run & sleep 5 && kafka-server-start /etc/kafka/server.properties"]

