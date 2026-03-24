from producer.producer import ProducerClass
import json
from Admin.adminclient import AdminClientClass
from confluent_kafka.schema_registry import SchemaRegistryClient
import jsonschema
from jsonschema import validate, ValidationError
from schemas.register_schema import SchemaRegistryManager



class User:
    def __init__(self, user_id,first_name, last_name, age, email_id, city):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.city = city
        self.email_id = email_id


def convert_json(user):
    user_payload = {
        "user_id" : user.user_id,
        "first_name" : user.first_name,
        "last_name" : user.last_name,
        "age": user.age,
        "city": user.city,
        "email": user.email_id
    }

    return  user_payload, json.dumps(user_payload).encode("utf-8")


def fetch_schema_from_registry(schema_registry_url, topic):
    client = SchemaRegistryClient({"url": schema_registry_url})
    subject = f"{topic}-value"

    try:
        # Fetch latest registered schema
        registered_schema = client.get_latest_version(subject)
        schema_str = registered_schema.schema.schema_str  
        print(f"Schema fetched from registry for subject: '{subject}'")
        return json.loads(schema_str)  
    except Exception as e:
        raise Exception(f"Failed to fetch schema for '{subject}': {e}")


def validate_user(user_payload: dict, schema: dict) -> bool:
    """Validate user payload against JSON schema."""
    try:
        validate(instance=user_payload, schema=schema)
        print("✅ Validation passed!")
        return True
    except ValidationError as e:
        print(f"Validation failed: {e.message}")
        return False



class JsonProducer(ProducerClass):
    def __init__(self,bootstrap_server, topic):
        super().__init__(bootstrap_server, topic)




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


