# We're making this file to listen for new messages in offline_messages and push them to RabbitMQ
import pika
import psycopg2
import json

from aws_cdk import aws_secretsmanager as secretsmanager
from deploy import ChatSystemStack

# Retrieve secrets
secret_manager = secretsmanager()
db_password = secret_manager.get_secret_value("DatabaseCredentials")['password']
rabbitmq_password = secret_manager.get_secret_value("BrokerCredentials")['password']

# Database connection
conn_string = f"dbname=ChatDatabase user=admin password={db_password} host=l"
conn = psycopg2.connect(conn_string)

# RabbitMQ connection
rabbitmq_host = 'l'
credentials = pika.PlainCredentials("admin", rabbitmq_password)
parameters = pika.ConnectionParameters(rabbitmq_host, 5672, '/', credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# Declare a queue
channel.queue_declare(queue='offline_messages', durable=True)

#creating a cursor to interract with the database
cursor = conn.cursor()

# Fetch offline messages and publish them
cursor.execute("SELECT message_id, recipient_id, message_content, metadata FROM offline_messages")
messages = cursor.fetchall()

for message_tuple in messages:
    message_id, recipient_id, message_content, metadata = message_tuple
    message = {
        "message_id": message_id,
        "recipient_id": recipient_id,
        "message_content": message_content,
        "metadata": metadata
    }
    channel.basic_publish(
        exchange='',
        routing_key='offline_messages',
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2  # Make message persistent
        )
    )
    print(f'Published the message {message_id} to RabbitMQ.')

# Close connections
connection.close()
conn.close()