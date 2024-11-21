# Используем официальный образ Python 3.9 на базе Red Hat UBI
FROM registry.access.redhat.com/ubi8/python-39:latest

# Рабочая директория
WORKDIR /app

# Устанавливаем pip и необходимые Python-библиотеки
RUN pip install --no-cache-dir --upgrade pip
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Копируем конфигурационный файл Kafka и Python-скрипт
COPY config/server.properties /app/config/server.properties
COPY topics.py /app/topics.py

# Указываем команду для запуска скрипта
CMD ["python3", "/app/topics.py"]
