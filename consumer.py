from flask import Flask
import pika
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

def callback(ch, method, properties, body):
    # Process the received message
    # Write the received message to a file
    with open('received_messages.txt', 'a') as file:
        file.write("Received message: " + body.decode() + "\n")
    # Manually acknowledge the message
    ch.basic_ack(delivery_tag=method.delivery_tag)

@app.route('/receive', methods=['POST'])
def receive_message():
    try:
        # Connect to RabbitMQ
        credentials = pika.PlainCredentials('myadmin', 'mypassword')
        parameters = pika.ConnectionParameters('10.250.4.93', 5672, '/', credentials)

        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.exchange_declare(exchange='POS-exchange', exchange_type='direct', durable=True)  # Set durable to True
        channel.queue_declare(queue='POS-queue')
        channel.queue_bind(queue='POS-queue', exchange='POS-exchange', routing_key='POS-key')
        channel.basic_consume(queue='POS-queue', on_message_callback=callback, auto_ack=False)
        print("Successful!")  # Moved the print statement here
        channel.start_consuming()
        return 'Message received'
    except pika.exceptions.AMQPError as e:
        print("Failed to connect to RabbitMQ:", str(e))
        return 'Error occurred'

if __name__ == '__main__':
    app.run(host='0.0.0.0')