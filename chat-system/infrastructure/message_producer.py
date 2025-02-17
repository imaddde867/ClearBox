# We're making this file to listen for new messages in offline_messages and push them to RabbitMQ
import time
import pika
from ChatDatabase.models import OfflineMessage 

