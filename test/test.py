import uvicorn
from confluent_kafka import Producer
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Message(BaseModel):
    msg: str

producer_config = {
    "bootstrap.servers": "0.0.0.0:9092"
}

producer = Producer(producer_config)

topic = "test"

@app.post("/kafka", tags=["Kafka"])
async def sender(msg: Message):
    message = msg.msg
    producer.produce(topic, message.encode('utf-8'))
    producer.flush()
    print(f"Сообщение '{message}' отправлено в топик '{topic}'")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=6001)
