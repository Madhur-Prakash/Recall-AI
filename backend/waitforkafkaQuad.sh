#!/bin/sh
host_kafka=kafka
port_kafka=29092
host_qdrant=qdrant-db
port_qdrant=6333

until nc -z "$host_kafka" "$port_kafka"; do
  echo "Waiting for Kafka..."
  sleep 3
done

until nc -z "$host_qdrant" "$port_qdrant"; do
  echo "Waiting for Qdrant..."
  sleep 3
done

echo "Dependencies are up, starting app..."
exec "$@"
