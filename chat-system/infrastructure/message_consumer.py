import pika
import json
import psycopg2
from aws_cdk import aws_secretsmanager as secretsmanager

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

# Declare queue
channel.queue_declare(queue='offline_messages', durable=True)

#creating a cursor to interract with the database
cursor = conn.cursor()

def deliver_message(ch, method, properties, body):
    try:
        message = json.loads(body)
        print(f"Processing message {message['message_id']} for {message['recipient_id']}")

        # Check if user is online 
        cursor.execute("SELECT is_active FROM users WHERE user_id = %s", (message['recipient_id'],))
        is_active_result = cursor.fetchone()
        
        if is_active_result and is_active_result[0]:  # Check if fetchone() returned a row and if is_active is True
            print(f"User {message['recipient_id']} is active, delivering message.")
            #Mark as delivered
            cursor.execute("UPDATE offline_messages SET delivered_at = NOW() WHERE message_id = %s", (message['message_id'],))
            conn.commit()
            ch.basic_ack(delivery_tag=method.delivery_tag) #Aknowledge message
        else:
            print(f"User {message['recipient_id']} is currently offline or does not exist, queuing message for later delivery.")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)  # Retry later
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error processing message: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)  # Don't requeue invalid messages
    except psycopg2.Error as e:
        print(f"Database error: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)  # Don't requeue on database errors

channel.basic_consume(queue='offline_messages', on_message_callback=deliver_message)
print("Waiting for messages...")
channel.start_consuming()