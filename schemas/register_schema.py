import os
import json
from confluent_kafka.schema_registry import SchemaRegistryClient, Schema


class SchemaRegistryManager:
    def __init__(self, schem_registry_url, schema_folder):
        self.schem_registry_url   = schem_registry_url
        self.schema_folder        = schema_folder
        self.schema_registry_conf = {'url': self.schem_registry_url}
        self.client               = SchemaRegistryClient(self.schema_registry_conf)

    def load_schema_files(self):
        schema_files = []
        for file_name in os.listdir(self.schema_folder):
            if file_name.endswith(".json"):
                file_path = os.path.join(self.schema_folder, file_name)
                with open(file_path, "r") as f:
                    data = json.load(f)
                    schema_files.append(data)
                    print(f"Loaded schema file: {file_name}")
        return schema_files

    def schema_exists(self, topic):
        subject = f"{topic}-value"
        try:
            self.client.get_latest_version(subject)
            return True
        except Exception:
            return False

    def register_schema(self, topic, schema, schema_type):
        subject = f"{topic}-value"
        json_schema = Schema(
            json.dumps(schema),
            schema_type=schema_type
        )
        try:
            schema_id = self.client.register_schema(subject, json_schema)
            print(f"Registered JSON schema for subject '{subject}' with ID: {schema_id}")
            return schema_id
        except Exception as e:                           
            print(f" Failed to register schema for '{subject}': {e}")
            return None

    def register_all(self, overwrite: bool = False):
        schemas = self.load_schema_files()
        if not schemas:
            print(" No schema found!")
            return

        print(f"\n🚀 Registering {len(schemas)} schema(s)...\n")

        for entry in schemas:
            topic       = entry.get("topic")
            schema      = entry.get("schema")
            schema_type = entry.get("schema_type", "JSON")

            if not topic or not schema:
                print(" Invalid topic or schema format, skipping...")
                continue

            if self.schema_exists(topic) and not overwrite:
                print(f"⏭ Schema for '{topic}' already exists, skipping...")
                continue

            self.register_schema(topic, schema, schema_type)

        print("\n All schemas processed!")              
