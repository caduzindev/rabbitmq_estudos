import pika

class RabbitmqConsumer:
  def __init__(self, queue, callback) -> None:
    self.__host = "localhost"
    self.__port = 5672
    self.__username = "guest"
    self.__password = "guest"
    self.__queue = queue
    self.__callback = callback
    self.__channel = self.__createChannel()

  def __createChannel(self):
    connection_parameters = pika.ConnectionParameters(
      host=self.__host,
      port=self.__port,
      credentials=pika.PlainCredentials(
        username=self.__username,
        password=self.__password
      )
    )
    channel = pika.BlockingConnection(connection_parameters).channel()
    channel.queue_declare(
      queue=self.__queue,
      durable=True
    )

    channel.basic_consume(
      queue=self.__queue,
      auto_ack=True,
      on_message_callback=self.__callback
    )

    return channel

  def start(self):
    print(f'Listen RabbitMQ on Port 5672')
    self.__channel.start_consuming()

def minha_callback(ch, method, properties, body):
  print(body)

rabbitmq_consumer = RabbitmqConsumer('data_queue', minha_callback)
rabbitmq_consumer.start()