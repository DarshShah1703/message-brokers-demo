import pika


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()


# Queue declaration
queue = channel.queue_declare(queue='order_report')
queue_name = queue.method.queue

channel.queue_bind(exchange='order', queue=queue_name, routing_key='order.report')


def callback(ch, method, properties, body):
    print(f"Received report message: {body.decode()}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(queue=queue_name, on_message_callback=callback)

print('Waiting for report messages...')
channel.start_consuming()
