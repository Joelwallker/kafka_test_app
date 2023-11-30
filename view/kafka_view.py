# kafka_view.py

class KafkaView:
    @staticmethod
    def display_stats(server, topic, rps, sent, consumed, lag_info):
        print(f"Server: {server}, Topic: {topic}, RPS: {rps}, Sent: {sent}, Consumed: {consumed}, Lag: {lag_info}")
