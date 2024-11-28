from kafka.admin import KafkaAdminClient, NewTopic
import time

time.sleep(60)

# Инициализация клиента администратора Kafka
admin_client = KafkaAdminClient(
    bootstrap_servers="kafka:9092",  # Используйте внешний адрес, если скрипт не внутри контейнера
    client_id='admin-client'  # Пример уникального идентификатора клиента
)

# Список существующих тем
topic_names = [
    "category-index", "category-seo", "goods-category-result", "goods-index", "goods-seo",
    "d-a-categories-index", "d-a-categories-seo", "d-a-goods-index", "d-a-goods-seo", "d-a-result",
    "d-g-categories-index", "d-g-categories-seo", "d-g-goods-index", "d-g-goods-seo", "d-g-result",
    "d-r-categories-index", "d-r-categories-seo", "d-r-goods-index", "d-r-goods-seo", "d-r-result",
    "d-s-categories-index", "d-s-categories-seo", "d-s-result", "d-s-services-index", "d-s-services-seo",
    "jud-index", "jud-seo", "phys-index", "phys-jud-result", "phys-seo",
    "vacancy-index", "vacancy-seo", "vacancy-resume-index", "vacancy-resume-seo", "vacancy-result",
    "translation", "translation-res",
]

# Преобразуем все строки в объекты NewTopic
topic_list = [NewTopic(name=topic, num_partitions=1, replication_factor=1) for topic in topic_names]

# Добавление новой темы
new_topic = NewTopic(name="example_topic", num_partitions=1, replication_factor=1)
topic_list.append(new_topic)

# Создание тем в Kafka
admin_client.create_topics(new_topics=topic_list, validate_only=False)
