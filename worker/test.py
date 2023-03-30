import pika
import json
import time
import os
from dotenv import load_dotenv

load_dotenv()
rb_host = os.getenv("RB_HOST")
rb_port = int(os.getenv("RB_PORT"))
credentials = pika.PlainCredentials(os.getenv("RB_USER"), os.getenv("RB_PASSWORD"))
parameters = pika.ConnectionParameters(host=rb_host, port=rb_port, credentials=credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

queue_name = 'test'
channel.queue_declare(queue=queue_name, durable=False)
channel.basic_qos(prefetch_count=1)

print(" [*] Waiting for messages in %s. To exit press CTRL+C" % queue_name)


def callback(ch, method, properties, body):
    print(" [x] Received %s" % body)
    payload = json.loads(body)
    queue_id = payload['queues_id']
    time.sleep(5)
    try:
        result = process_queue(queue_id)
        print(result)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(" [#] Error during execution: %s" % e)
        ch.basic_nack(delivery_tag=method.delivery_tag)


def process_queue(queue_id):
    # TODO: Implement this function
    return "Queue %s processed" % queue_id
    pass


channel.basic_consume(queue=queue_name, on_message_callback=callback)

try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()

connection.close()
