# Kafka Learning

Hands-on examples for Apache Kafka using **Confluent’s Python client** (`confluent-kafka`): topic administration, a JSON producer that validates payloads against schemas in **Confluent Schema Registry**, and a consumer driven by YAML configuration.

## Prerequisites

- **Python** 3.12+
- **[Poetry](https://python-poetry.org/)** for dependency management
- **Docker** and **Docker Compose** for the local Kafka stack

## Quick start: local Kafka stack

From the project root:

```bash
docker compose up -d
```

This starts:

| Service          | Purpose                          | Host port |
|------------------|----------------------------------|-----------|
| Zookeeper        | Coordination for Kafka           | 2181      |
| Kafka            | Message broker                   | 9092      |
| Schema Registry  | Avro/JSON schema storage & APIs  | 8081      |
| Kafka UI         | Web UI for topics, messages, etc.| 8080      |

- **Kafka (from your machine):** `localhost:9092`
- **Schema Registry:** `http://localhost:8081`
- **Kafka UI:** `http://localhost:8080`

Stop the stack:

```bash
docker compose down
```

## Python environment

Install dependencies:

```bash
poetry install
```

Run entry points from the project root (examples):

```bash
poetry run python main.py
poetry run python main_consumer.py
```

You can also run individual scripts from the project root (ensure Kafka is up first where needed):

```bash
poetry run python producer/jsonProducer.py
poetry run python test.py
```

## Project layout

| Path | Role |
|------|------|
| `docker-compose.yaml` | Zookeeper, Kafka, Schema Registry, Kafka UI |
| `main.py` | Registers schemas, ensures topic exists, interactive **JSON** producer for `user-info-topic` |
| `main_consumer.py` | Loads `user_engagement` consumer settings from config and runs `BaseConsumer` |
| `config/config.yaml` | Bootstrap server, Schema Registry URL, consumer names, optional S3-related keys |
| `config/config_loader.py` | Loads YAML; used by consumer code |
| `Admin/adminclient.py` | `AdminClientClass` — create topics if missing |
| `producer/producer.py` | `ProducerClass` — plain string produce + flush |
| `producer/jsonProducer.py` | `JsonProducer`, `User` model, schema fetch/validation helpers |
| `schemas/register_schema.py` | `SchemaRegistryManager` — register JSON schemas from `schemas/` |
| `schemas/user-info-topic.json` | Topic name + JSON Schema for user records |
| `consumer/consumer.py` | `BaseConsumer` — subscribe and print decoded messages |
| `test.py` | Lists JSON schema files in the configured schemas folder |

## Configuration

- **Bootstrap** and **Schema Registry** URLs live in `config/config.yaml` under `kafka`.
- **Consumers** are defined under `consumers` (e.g. `user_engagement` with `topic`, `group_id`, and related keys).
- `ConfigLoader` accepts a path to `config.yaml`. If you use the default constructor, ensure that path matches your machine, or instantiate it with the correct path, for example:

  ```python
  ConfigLoader("/Users/you/kafka-Learning/config/config.yaml")
  ```

- `main.py` and `test.py` use a **schema folder path** when registering or listing schemas. Point those variables at your clone’s `schemas/` directory (or refactor to `Path(__file__).resolve().parent / "schemas"`).

## Dependencies (high level)

- `confluent-kafka` — producer, consumer, admin client, Schema Registry integration
- `jsonschema` — validate payloads before produce
- `pyyaml` — load `config/config.yaml`
- `httpx`, `authlib`, `cachetools`, `certifi` — dependency tree / HTTP as needed

## License

Not specified in the repository; add a `LICENSE` file if you plan to share the project.
