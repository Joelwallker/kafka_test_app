# kafka_model.py

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import asyncio

class KafkaModel:
    def __init__(self, server):
        self.server = server
        self.producer = AIOKafkaProducer(bootstrap_servers=server)

    async def send_message(self, topic, message):
        await self.producer.send_and_wait(topic, message.encode('utf-8'))

    async def get_topics(self):
        consumer = AIOKafkaConsumer(bootstrap_servers=self.server)
        await consumer.start()
        topics = await consumer.topics()
        await consumer.stop()
        return topics
