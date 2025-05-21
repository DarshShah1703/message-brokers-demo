import pika

# Connect to local RabbitMQ instance
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare a direct exchange
channel.exchange_declare(exchange='order', exchange_type='direct')

# Messages to send
message1 = 'User email: user@example.com'
message2 = 'Order details: ID125, item ABC'

# # Publish messages with routing keys
channel.basic_publish(exchange='order', routing_key='order.notify', body=message1)
print(' [X] sent notify message')

channel.basic_publish(exchange='order', routing_key='order.report', body=message2)
print(' [X] sent notify message')


connection.close()
