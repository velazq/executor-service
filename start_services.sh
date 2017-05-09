#!/bin/sh

echo "Starting RabbitMQ container..."
docker run -d -p 5672:5672 --restart unless-stopped rabbitmq

echo "Starting Redis container..."
docker run -d -p 6379:6379 --restart unless-stopped redis
