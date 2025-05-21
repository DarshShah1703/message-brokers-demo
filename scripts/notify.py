import pika



connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Queue declaration
queue = channel.queue_declare(queue='order_notify')
queue_name = queue.method.queue

channel.queue_bind(exchange='order', queue=queue_name, routing_key='order.notify')

def callback(ch, method, properties, body):
    print(f"Received notify message: {body.decode()}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


# Bind to exchange with routing key

# Consume messages
channel.basic_consume(queue=queue_name, on_message_callback=callback)

print('Waiting for notify messages...')
channel.start_consuming()
