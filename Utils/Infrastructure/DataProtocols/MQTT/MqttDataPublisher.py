from Utils.Infrastructure.DataProtocols.DataPublisher import DataPublisher
from Utils.Infrastructure.DataProtocols.MQTT.MqttDataProtocol import MqttDataProtocol
from Utils.Settings import Config
import pika

class MqttDataPublisher(DataPublisher):

    def __init__(self, ip, topic):
        DataPublisher.__init__(self, MqttDataProtocol())
        self.ip = ip
        self.topic = topic
        self.connection = pika.BlockingConnection(pika.URLParameters(self.ip))

        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.topic)

    def publish(self, message):
        with self.lock:
            self.channel.basic_publish(exchange='',
                                  routing_key=self.topic,
                                  body=self.protocol.encodeMessage(message))
            # print("Sent message via mqtt : {}".format(message.request_id))

    def close(self):
        self.connection.close()