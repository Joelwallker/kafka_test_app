# main.py
import asyncio
from model.kafka_model import KafkaModel
from view.kafka_view import KafkaView
from controller.kafka_controller import KafkaController
import json
from datetime import datetime
import random

# Генерация сложного JSON сообщения
def generate_complex_message():
    return json.dumps({
        "timestamp": str(datetime.now()),
        "sensor_id": random.randint(1000, 9999),
        "values": [random.random() for _ in range(10)],
        "metadata": {
            "location": "sensor-" + str(random.randint(1, 100)),
            "status": random.choice(["active", "inactive"])
        }
    })

async def main():
    servers = [
        "stress.kafka1.faberlic.ru",
        "stress.kafka2.faberlic.ru",
        "stress.kafka3.faberlic.ru",
        # Добавьте дополнительные серверы здесь, если необходимо
    ]
    duration = 60  # Продолжительность в секундах

    for server in servers:
        model = KafkaModel(server)
        view = KafkaView()
        controller = KafkaController(model, view)

        await model.producer.start()
        topics = await model.get_topics()
        for topic in topics:
            message = generate_complex_message()  # Генерация сообщения для отправки
            await controller.perform_test(server, topic, message, duration)
        await model.producer.stop()

if __name__ == "__main__":
    asyncio.run(main())
