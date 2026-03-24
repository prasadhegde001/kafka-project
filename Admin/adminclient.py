from confluent_kafka.admin import AdminClient, NewTopic

class AdminClientClass:
    def __init__(self, bootstrap_server):
        self.bootstrap_server = bootstrap_server
        self.admin = AdminClient({"bootstrap.servers": self.bootstrap_server})

    def topic_exists(self, topic):
        meta_data = self.admin.list_topics()
        return topic in meta_data.topics.keys()
    
    def create_topic(self, topic, partitions=1):
        if not self.topic_exists(topic):
            new_topic = NewTopic(topic, num_partitions=partitions)
            self.admin.create_topics([new_topic])
            print(f"New topic is created:- {new_topic}")
        else:
            print(f"{topic} this topic already Present")
