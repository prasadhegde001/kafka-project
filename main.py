from producer.jsonProducer import User, convert_json, fetch_schema_from_registry, validate_user, JsonProducer
from producer.producer import ProducerClass
import json
from Admin.adminclient import AdminClientClass
from confluent_kafka.schema_registry import SchemaRegistryClient
import jsonschema
from jsonschema import validate, ValidationError
from schemas.register_schema import SchemaRegistryManager



if __name__ == "__main__":

    bootstrap_server = "localhost:9092"
    topic = "user-info-topic"
    schema_registry_url = 'http://localhost:8081'


    schema_folder = '/Users/prasad.hegde/Documents/Kafka-Tutorial/schemas'

    schem_register = SchemaRegistryManager(
        schem_registry_url = schema_registry_url,
        schema_folder      = schema_folder
    )
    schem_register.register_all()

    schema = fetch_schema_from_registry(schema_registry_url, topic)
    
    a = AdminClientClass(bootstrap_server)
    a.create_topic(topic)

    p = JsonProducer(bootstrap_server, topic)

    try:
        while True:
            user_id = input("Enter user id: ")
            first_name = input("Enter your first_name: ")
            last_name = input("Enter last name: ")
            age = int(input("Enter age: "))
            city = input("Enter your city: ")
            email_id = input("Enter your email: ")

            user = User(user_id=user_id ,first_name=first_name, last_name=last_name, age=age, email_id=email_id, city=city)

            user_payload, json_message = convert_json(user)
            if validate_user(user_payload, schema):
                p.send_messages(json_message)
            else:
                print("Message NOT sent due to validation failure.\n")
    except KeyboardInterrupt:
        pass
    p.commit()