from confluent_kafka import Consumer, KafkaError, KafkaException
import json
from config.config_loader import ConfigLoader

class BaseConsumer:

    def __init__(self, bootstrap_server, group_id, topic):
        self.bootstrap_server = bootstrap_server
        self.topic = topic
        self.group_id = group_id
        self.consumer = Consumer({'bootstrap.servers': self.bootstrap_server,'group.id': self.group_id})

    
    def consume_messages(self):
        self.consumer.subscribe([self.topic])
        try:
            while True:
                msg = self.consumer.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    print(f"Consumer Error: {msg.error()}")
                    continue
                
                print(f"Message Consumed {msg.value().decode('utf-8')}")

        except KeyboardInterrupt:
            pass
        finally:
            self.consumer.close()



if __name__ == "__main__":

    config = ConfigLoader()
    consumer_config = config.get_consumer_config("user_engagement")

    bootstrap_server = config.get_bootstrap_server()
    topic = consumer_config["topic"]
    group_id = consumer_config["group_id"]
    


    # bootstrap_server = "localhost:19092"
    # topic = "test-topic"
    # group_id = 'my_group'

    # consumer = KafkaConsumer(bootstrap_server, group_id, topic)
    # consumer.consume_messages()
    
