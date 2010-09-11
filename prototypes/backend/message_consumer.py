from carrot.connection import BrokerConnection
from carrot.messaging import Consumer

conn = BrokerConnection(hostname="localhost", port=5672, \
                        userid="guest",password="guest", virtualhost="/")

consumer = Consumer(connection = conn, queue = "feed", exchange = "feed", \
                    routing_key = "importer")

def receiver_callback(message_data, message):
    print message_data['payload']
    message.ack()

consumer.register_callback(receiver_callback)
consumer.wait()
