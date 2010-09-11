from carrot.connection import BrokerConnection
from carrot.messaging import Publisher
import sys

conn = BrokerConnection(hostname="localhost", port=5672, \
                        userid="guest",password="guest", virtualhost="/")

publisher = Publisher(connection = conn, exchange="feed", routing_key="importer")

msg = ""
while msg != "exit":
    msg = sys.stdin.readline().strip()
    publisher.send({"payload":msg})
publisher.close()
