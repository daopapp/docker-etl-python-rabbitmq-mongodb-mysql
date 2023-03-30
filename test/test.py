import sys
import os
import pika
import json
from dotenv import load_dotenv

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)
from infra.utils import generate_id

load_dotenv()
rb_host = os.getenv("RB_HOST")
rb_port = int(os.getenv("RB_PORT"))
rb_user = os.getenv("RB_USER")
rb_password = os.getenv("RB_PASSWORD")
print(rb_host, rb_port, rb_user, rb_password)
if not rb_host or not rb_port or not rb_user or not rb_password:
    raise ValueError("One or more required environment variables are missing")

credentials = pika.PlainCredentials(rb_user, rb_password)
parameters = pika.ConnectionParameters(host=rb_host, port=rb_port, credentials=credentials)
connection = pika.BlockingConnection(parameters)

try:
    print("processando")
    channel = connection.channel()
    queue_name = 'test'

    r = generate_id()
    message = {'queue_id': r}
    print(message)
    message = json.dumps(message)
    channel.queue_declare(queue_name, durable=False)
    channel.basic_publish(exchange='', routing_key=queue_name, body=message)
    print(" [x] Sent %s" % message)
except Exception as e:
    print('Erro:', e)
finally:
    connection.close()
