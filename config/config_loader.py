import yaml
import os


class ConfigLoader:
    def __init__(self, config_path: str = "/Users/prasad.hegde/Documents/Kafka-Tutorial/config/config.yaml"):
        self.config_path = config_path
        self.config      = self._load()

    def _load(self) -> dict:

        if not os.path.exists(self.config_path):
            
            raise FileNotFoundError(f"Config file not found: {self.config_path}")

        with open(self.config_path, "r") as f:
            config = yaml.safe_load(f)
            print(f"Config loaded from: {self.config_path}")
            return config


    def get_bootstrap_server(self) -> str:
        return self.config["kafka"]["bootstrap_server"]

    def get_schema_registry_url(self) -> str:
        return self.config["kafka"]["schema_registry_url"]


    def get_consumer_config(self, consumer_name: str) -> dict:

        consumers = self.config.get("consumers", {})
        if consumer_name not in consumers:
            raise KeyError(f"Consumer '{consumer_name}' not found in config!")
        return consumers[consumer_name]

    def get_s3_config(self) -> dict:
        return self.config.get("s3", {})
    
