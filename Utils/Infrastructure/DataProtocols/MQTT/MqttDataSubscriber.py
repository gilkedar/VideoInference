from Utils.Infrastructure.DataProtocols.DataSubscriber import DataSubscriber
from Utils.Infrastructure.DataProtocols.MQTT.MqttDataProtocol import MqttDataProtocol
import threading
import pika


class MqttDataSubscriber(DataSubscriber):

    PREFETCH_VAL = 100

    def __init__(self, ip, topic, callback_function, queue=10):
        DataSubscriber.__init__(self, MqttDataProtocol(), callback_function, queue)
        self.ip = ip
        self.topic = topic

        self.connection = pika.BlockingConnection(pika.URLParameters(self.ip))
        self.channel = self.connection.channel()

        self.channel.queue_declare(queue=self.topic,durable=True)
        # self.lock = threading.Lock()

    def subscribe(self):
        self.channel.basic_qos(prefetch_count=self.PREFETCH_VAL, prefetch_size=0)
        self.channel.basic_consume(queue=self.topic,  on_message_callback=self.mqtt_callback)
        self.channel.start_consuming()

    def mqtt_callback(self,ch,method,properties,body):
        msg = self.protocol.decodeMessage(body)
        threading.Thread(target=self.callback_function, args=(msg,)).start()
        self.send_ack_for_ducument(ch,method)

    def send_ack_for_ducument(self, ch, method):

        # print "\nDelivery Tag: ({})  \n".format(method.delivery_tag)
        ch.basic_ack(delivery_tag=method.delivery_tag, multiple=True)