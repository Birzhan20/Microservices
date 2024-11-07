#-*- coding: utf-8 -*-
import uuid
import nest_asyncio
import g4f
import redis
import json
from confluent_kafka import Consumer, Producer, KafkaError, KafkaException
import logging

nest_asyncio.apply()

# Конфигурация Kafka
kafka_config = {
    'bootstrap.servers': 'kafka:9092',  # Адрес вашего брокера Kafka
    'group.id': 'phys_jud',  # ID группы потребителей
    'auto.offset.reset': 'earliest',  # Начинать с самого начала
    'enable.auto.commit': False,  # Отключаем авто-коммит, чтобы вручную подтвердить обработку
    'acks': 'all',  # Ждем подтверждения от всех брокеров
}

# Redis клиент (если нужно хранить processed message ID)
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

# Создание экземпляров Producer и Consumer для Kafka
producer = Producer(kafka_config)
consumer = Consumer(kafka_config)

consumer.subscribe(['phys-seo', 'jud-seo', 'jud-index', 'phys-index'])

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def process_message(text: str, category: str) -> str:
    """
    Функция для генерации мета-описания с помощью модели GPT.
    """
    try:
        if category == 'phys-seo':
            prompt = f"Напиши уникальный seo-текст не более 500 слов о возможности на международной платформе Mytrade.kz смотреть объявления о продаваемых товарах, услугах, недвижимости, автомобилей и т.д. на страницах частных лиц: {text}"
        elif category == 'phys-index':
            prompt = f"Напиши уникальный индексируемый мета-текст для текста: «{text}». При генерации ответа не используй ID пользователя."
        elif category == 'jud-seo':
            prompt = f"Напиши уникальный seo-текст не более 500 слов о возможности найти товары и услуги от магазинов и компаний со всего мира на Mytrade.kz: {text}"
        elif category == 'jud-index':
            prompt = f"Напиши уникальный индексируемый мета-текст для текста: «{text}». Без использования ID пользователя."
        else:
            return "Неизвестная категория."

        response = g4f.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            stream=False
        )

        return response.strip('"')
    except Exception as e:
        logger.error(f"Ошибка при генерации текста: {str(e)}")
        return f"Ошибка: {str(e)}"


def handle_message(message):
    """
    Обработка сообщения из Kafka.
    """
    try:
        # Преобразуем сообщение в JSON
        message_value = message.value().decode('utf-8')
        data = json.loads(message_value)

        message_id = data.get('message_id')  # Уникальный идентификатор сообщения
        text = data.get('text', '')
        category = data.get('category', '')

        if not text or not message_id:
            logger.warning(f"Сообщение не содержит текста или message_id. Игнорируем.")
            return

        # Проверяем, обрабатывалось ли это сообщение ранее
        if redis_client.exists(message_id):
            logger.info(f"Сообщение {message_id} уже обработано. Пропускаем.")
            return

        # Обрабатываем текст
        meta_description = process_message(text, category)

        # Отправляем результат обратно в Kafka
        result = {
            'message_id': str(uuid.uuid4()),  # Новый уникальный ID для возвращаемого сообщения
            'meta': meta_description,
            'category': category
        }

        # Отправка результата в другую тему Kafka
        producer.produce('phys-jud', json.dumps(result).encode('utf-8'))
        producer.flush()  # Ждем, пока сообщение не будет отправлено

        # Подтверждаем, что сообщение обработано
        consumer.commit()

    except KafkaException as e:
        logger.error(f"Ошибка Kafka: {str(e)}")
    except Exception as e:
        logger.error(f"Ошибка при обработке сообщения: {str(e)}")


def consume_messages():
    """
    Основная функция для получения сообщений из Kafka и их обработки.
    """
    logger.info("Начинаем потребление сообщений...")

    while True:
        try:
            msg = consumer.poll(timeout=1.0)  # Ждем сообщения с таймаутом 1 секунда

            if msg is None:
                continue  # Нет сообщений, продолжаем ожидать

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    logger.info(f"Достигнут конец для партиции {msg.partition}")
                else:
                    logger.error(f"Ошибка Kafka: {msg.error()}")
            else:
                handle_message(msg)

        except KeyboardInterrupt:
            logger.info("Завершаем потребление сообщений...")
            break
        except Exception as e:
            logger.error(f"Ошибка: {str(e)}")


if __name__ == '__main__':
    try:
        consume_messages()
    except Exception as e:
        logger.error(f"Ошибка: {str(e)}")
    finally:
        consumer.close()  # Закрываем consumer при завершении работы
