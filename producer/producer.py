from confluent_kafka import Producer
from Admin.adminclient import AdminClientClass


class ProducerClass:

    def __init__(self, bootstrap_server, topic):
        self.bootstrap_server = bootstrap_server
        self.topic = topic
        self.produce = Producer({'bootstrap.servers': self.bootstrap_server})

    def send_messages(self,message):
        try:
            self.produce.produce(self.topic, message)
            print(f"Message sent to topic {self.topic}: {message}")
        except Exception as e:
            print(f"Error sending message: {e}")

    def commit(self):
        self.produce.flush()
        print("Messages committed to Kafka.")
        
