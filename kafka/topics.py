from kafka import KafkaAdminClient
from kafka.admin import NewTopic
import time

# Список топиков
topics_list = [
    "category-index", "category-seo", "goods-category-result", "goods-index", "goods-seo",
    "d-a-categories-index", "d-a-categories-seo", "d-a-goods-index", "d-a-goods-seo", "d-a-result",
    "d-g-categories-index", "d-g-categories-seo", "d-g-goods-index", "d-g-goods-seo", "d-g-result",
    "d-r-categories-index", "d-r-categories-seo", "d-r-goods-index", "d-r-goods-seo", "d-r-result",
    "d-s-categories-index", "d-s-categories-seo", "d-s-result", "d-s-services-index", "d-s-services-seo",
    "jud-index", "jud-seo", "phys-index", "phys-jud-result", "phys-seo",
    "vacancy-index", "vacancy-seo", "vacancy-resume-index", "vacancy-resume-seo", "vacancy-result",
    "translation", "translation-res",
]

def create_topics(bootstrap_servers, topics):
    # Создаем клиента администратора
    admin_client = KafkaAdminClient(bootstrap_servers=bootstrap_servers)

    # Составляем список новых топиков
    new_topics = [NewTopic(name=topic, num_partitions=3, replication_factor=2) for topic in topics]

    # Создаем топики
    try:
        admin_client.create_topics(new_topics=new_topics, validate_only=False)
        print("Topics created successfully.")
    except Exception as e:
        print(f"Error creating topics: {e}")
    finally:
        admin_client.close()

if __name__ == "__main__":
    # Задержка, чтобы Kafka успел полностью запуститься
    print("Waiting for Kafka to be ready...")
    time.sleep(10)

    # Создание топиков
    create_topics('kafka:9092', topics_list)
