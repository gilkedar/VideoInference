from Utils.Infrastructure.DataProtocols.DataSubscriber import DataSubscriber
from Utils.Infrastructure.DataProtocols.MQTT.MqttDataProtocol import MqttDataProtocol
import threading


class MqttDataSubscriber(DataSubscriber):

    def __init__(self, callback_function, queue=10):
        DataSubscriber.__init__(self, MqttDataProtocol, callback_function, queue)

    def subscribe(self):
        self.listen_flag = True

        while self.listen_flag:
            pass