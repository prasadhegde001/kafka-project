from confluent_kafka import Consumer, KafkaError, KafkaException
import json
from config.config_loader import ConfigLoader
from consumer.consumer import BaseConsumer


if __name__ == "__main__":

    config = ConfigLoader()
    consumer_config = config.get_consumer_config("user_engagement")

    bootstrap_server = config.get_bootstrap_server()
    topic = consumer_config["topic"]
    group_id = consumer_config["group_id"]

    consumer = BaseConsumer(bootstrap_server, group_id, topic)
    consumer.consume_messages()