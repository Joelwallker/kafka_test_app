# kafka_controller.py

import time
import asyncio
from confluent_kafka import Consumer, Producer, KafkaError, KafkaException
from confluent_kafka.admin import AdminClient, NewTopic
from kafka import KafkaConsumer, TopicPartition

class KafkaController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    async def perform_test(self, server, topic, message, duration):
        start_time = time.time()
        count = 0

        while time.time() - start_time < duration:
            await self.model.send_message(topic, message)
            count += 1
            await asyncio.sleep(0.01)  # Adjust as needed

        rps = count / duration

        # Получение и анализ lag потребителей
        lag_info = self.get_consumer_lag(server)
        self.view.display_stats(server, topic, rps, count, count, lag_info)

    def get_consumer_lag(self, bootstrap_servers):
        admin_client = AdminClient({'bootstrap.servers': bootstrap_servers})

        # Получение информации о всех группах потребителей
        try:
            consumer_groups = admin_client.list_groups(timeout=10)
        except KafkaException as e:
            print(f"Ошибка при получении групп потребителей: {e}")
            return {}

        lag_info = {}
        for group in consumer_groups:
            group_id = group.id
            consumer = KafkaConsumer(group_id=group_id, bootstrap_servers=bootstrap_servers)

            try:
                for topic_partition in consumer.assignment():
                    committed = consumer.committed(topic_partition)
                    if committed is not None:
                        committed_offset = committed.offset
                        tp = TopicPartition(topic_partition.topic, topic_partition.partition)
                        end_offsets = consumer.end_offsets([tp])
                        latest_offset = end_offsets[tp]
                        lag = latest_offset - committed_offset
                        lag_info[(group_id, topic_partition)] = lag
            finally:
                consumer.close()

        return lag_info
