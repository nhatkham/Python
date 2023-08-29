#!/usr/bin/python3

from flask import Flask, request, jsonify
import pika

app = Flask(__name__)

#Connect to RMQ

credentials=pika.PlainCredentials('myadmin', 'mypassword')
parameters = pika.ConnectionParameters('10.250.4.93', 5672, '/', credentials)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()


@app.route('/api/pos/', methods=['POST'])
def pos_endpoint():
        # Retrieve the payload from the request
       payload = request.get_json()

        # Process the payload and generate a response
        # ...

        # Publish the payload as a message to RabbitMQ
       channel.basic_publish(exchange='', routing_key='pos-q', body=str(payload))
        # Return the response as JSON
       return jsonify({'Message published to RabbitMQ': 'success'})

if __name__ == '__main__':
    app.run(host='0.0.0.0')