from Utils.Infrastructure.DataProtocols.DataSubscriber import DataSubscriber
from Utils.Infrastructure.DataProtocols.MQTT.MqttDataProtocol import MqttDataProtocol
import threading
import pika


class MqttDataSubscriber(DataSubscriber):

    def __init__(self, ip, topic, callback_function, queue=10):
        DataSubscriber.__init__(self, MqttDataProtocol(), callback_function, queue)
        self.ip = ip
        self.topic = topic

        self.connection = pika.BlockingConnection(pika.URLParameters(self.ip))
        self.channel = self.connection.channel()

        self.channel.queue_declare(queue=self.topic)

    def subscribe(self):

        self.channel.basic_consume(queue=self.topic, auto_ack=True, on_message_callback=self.mqtt_callback)
        self.channel.start_consuming()

    def mqtt_callback(self,ch,method,properties,body):

        msg = self.protocol.decodeMessage(body)
        threading.Thread(target=self.callback_function, args=(msg,)).start()

