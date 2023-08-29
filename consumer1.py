import pika
from datetime import datetime

mes_count = 0

def callback(ch, method, properties, body):
    # Process the received message
    # Write the received message to a file
    global mes_count
    print('Message consumed')
    mes_count += 1
    timestamp = datetime.now().strftime("%H:%M:%S.%f")  # Get the current timestamp

    message = f"Received message {mes_count} at {timestamp}: {body.decode()}\n"

    with open('received_messages.txt', 'a') as file:
        file.write(message)
    # Manually acknowledge the message
    ch.basic_ack(delivery_tag=method.delivery_tag)

try:
    # Connect to RabbitMQ
    credentials = pika.PlainCredentials('myadmin', 'mypassword')
    parameters = pika.ConnectionParameters('10.250.4.93', 5672, '/', credentials)

    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.exchange_declare(exchange='pos-ex', exchange_type='direct', durable=True)
    channel.queue_declare(queue='pos-q')
    channel.queue_bind(queue='pos-q', exchange='pos-ex', routing_key='pos-key')
    channel.basic_consume(queue='pos-q', on_message_callback=callback, auto_ack=False)
    print('Waiting for message...')
    channel.start_consuming()
except pika.exceptions.AMQPError as e:
    print("Failed to connect to RabbitMQ:", str(e))