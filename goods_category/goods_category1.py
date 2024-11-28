#-*- coding: utf-8 -*-
import uuid
import nest_asyncio
import g4f
import redis
import json
from confluent_kafka import Consumer, Producer, KafkaError, KafkaException
import logging

nest_asyncio.apply()


consumer_config = {
    'bootstrap.servers': '0.0.0.0:9092',
    'group.id': 'goods_category',
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': False,
}

producer_config = {
    'bootstrap.servers': '0.0.0.0:9092',
    'acks': 'all',
}

# Redis клиент (если нужно хранить processed message ID)
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

# Создание экземпляров Producer и Consumer для Kafka
producer = Producer(producer_config)
consumer = Consumer(consumer_config)

consumer.subscribe(['goods-seo', 'goods-index', 'category-seo', 'category-index'])

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def process_message(text: str, category: str) -> str:
    try:
        if category == 'goods-index':
            prompt = f"Напиши уникальное индексируемое в google мета-описание не более 200 слов для товара, продаваемого на международном маркете Mytrade.kz на основе этого текста: {text}"
        elif category == 'goods-seo':
            prompt = f"Напиши уникальный seo-текст не более 500 слов о возможности найти на международном маркете Mytrade товар «{text}» продаваемый магазинами со всего мира, включая Казахстан. Приведи примеры применения товара «{text}». Перечисли кратко несколько городов мира, в которых магазины продают этот товар в маркете Mytrade.kz. В тексте не используй заголовки для разделов, не используй слово 'Нур-султан', не используй иконки, не используй переносы строк на новую строку, не используй пункты, не используй жирный шрифт. Текст должен быть полностью слитным."
        elif category == 'category-index':
            prompt = f"Напиши уникальное индексируемое в google мета-описание не более 200 слов для категории международного маркета Mytrade.kz «{text}». Напиши кратко какие товары можно купить в данной категории."
        elif category == 'category-seo':
            prompt = f"Напиши уникальный seo-текст из 500 слов о продаже товаров из категории «{text}» на международном маркете Mytrade.kz. Расскажи о широком ассортименте товаров в категории «{text}» от продавцов и производителей со всего мира. Перечисли продаваемые в маркете Mytrade.kz товары из категории «{text}» и приведи примеры их применения. Перечисли кратко несколько городов мира, в которых магазины продают товары из данной категории на маркете Mytrade.kz. В тексте не используй заголовки для разделов, не используй слово 'Нур-султан', не используй иконки, не используй переносы строк на новую строку, не используй пункты, не используй жирный шрифт. Текст должен быть полностью слитным"
        else:
            return "unknown category"

        response = g4f.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            stream=False
        )

        return response.strip('"')
    except Exception as e:
        logger.error(f"Ошибка при генерации текста: {str(e)}")
        return f"Error {str(e)}"


def handle_message(message):
    try:
        message_value = message.value().decode('utf-8')
        data = json.loads(message_value)

        message_id = data.get("message_id")
        text = data.get("text", "")
        category = data.get("category", "")

        if not text or not message_id:
            logger.warning(f"None, ignore...")
            return

        if redis_client.exists(message_id):
            logger.info(f"Message {message_id} has already been processed. skip it")
            return

        meta_description = process_message(text, category)

        result = {
            'message_id': str(uuid.uuid4()),
            'meta': meta_description,
            'category': category
        }

        producer.produce('goods-category-result', json.dumps(result).encode('utf-8'))
        producer.flush()

        consumer.commit()

    except KafkaException as e:
        logger.error(f"Error Kafka: {str(e)}")
    except Exception as e:
        logger.error(f"Error of processing message: {str(e)}")


def consume_messages():
    logger.info("Starting consume messages...")

    while True:
        try:
            msg = consumer.poll(timeout=1.0)

            if msg is None:
                continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    logger.info(f"The end of partitions has been reached {msg.partition}")
                else:
                    logger.error(f"Error Kafka: {msg.error()}")
            else:
                handle_message(msg)

        except KeyboardInterrupt:
            logger.info("Completing the consumption of messages...")
            break
        except Exception as e:
            logger.error(f"Error: {str(e)}")


if __name__ == '__main__':
    try:
        consume_messages()
    except Exception as e:
        logger.error(f"Error: {str(e)}")
    finally:
        consumer.close()
