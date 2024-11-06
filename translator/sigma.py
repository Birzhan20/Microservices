#-*- coding: utf-8 -*-
import json
import logging
import uuid
from logging.handlers import RotatingFileHandler
import redis
from deep_translator import GoogleTranslator
from confluent_kafka import Consumer, Producer, KafkaError, KafkaException
from langs import lang_mapping

logging.basicConfig(
    handlers=[RotatingFileHandler("sigma.log", maxBytes=5_000_000, backupCount=5)],
    encoding="utf-8",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

langs = list(lang_mapping.keys())

kafka_config = {
    'bootstrap.servers': 'kafka:9092',
    'group.id': 'translator-consumer',
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': False,
    'acks': 'all',  # Ждем подтверждения от всех брокеров
}

# Redis client to store processed message IDs
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

producer = Producer(kafka_config)
consumer = Consumer(kafka_config)

consumer.subscribe(['translation'])


def delivery_report(err, msg):
    if err:
        logging.error(f"Delivery failed for message: {err}")
    else:
        logging.info(f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")


def send_translation_result(translations):
    try:
        result_message = {
            'message_id': str(uuid.uuid4()),
            'translations': translations,
        }
        producer.produce(
            'translation-res',
            value=json.dumps(result_message),
            callback=delivery_report
        )
        producer.flush()  # Ensure message is sent before continuing
        logging.info("Translation result sent to Kafka.")
    except Exception as e:
        logging.error(f"Failed to send translation result to Kafka: {e}")


def process_translation_request(message):
    message_id = message.get('message_id')

    if not message_id:
        logging.error("Message is missing a unique message_id, skipping.")
        return

    # Check if this message was already processed (idempotency)
    if redis_client.get(message_id):
        logging.info(f"Message {message_id} already processed. Skipping.")
        return

    src = message.get('src_lang')
    text = message.get('input_text')

    google_src = lang_mapping.get(src)

    if not google_src:
        logging.error(f"Unacceptable source language: {src}")
        return

    translations = {}

    for tgt in langs:
        if tgt != src:
            google_tgt = lang_mapping[tgt]
            try:
                result = GoogleTranslator(source=google_src, target=google_tgt).translate(text)
                translations[tgt] = result
            except Exception as e:
                logging.error(f"Error when translating into {google_tgt}: {e}")
                translations[tgt] = "Translation error"

    send_translation_result(translations)

    # Store in Redis to avoid reprocessing
    try:
        redis_client.set(message_id, "processed", ex=3600)  # Set an expiration of 1 hour
        logging.info(f"Message {message_id} marked as processed.")
    except Exception as e:
        logging.error(f"Error storing message ID {message_id} in Redis: {e}")

    # Commit offset only after processing and sending the result
    consumer.commit()


def run_kafka_consumer():
    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    logging.info(f"End of partition reached: {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")
                else:
                    raise KafkaException(msg.error())
            else:
                message = json.loads(msg.value().decode('utf-8'))
                process_translation_request(message)
    except KeyboardInterrupt:
        logging.info("Kafka consumer interrupted by user.")
    except Exception as e:
        logging.error(f"Error during Kafka consumption: {e}")
    finally:
        consumer.close()


if __name__ == "__main__":
    logging.info("Kafka consumer started")
    run_kafka_consumer()
