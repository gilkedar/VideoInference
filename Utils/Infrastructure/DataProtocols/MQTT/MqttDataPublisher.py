from Utils.Infrastructure.DataProtocols.DataPublisher import DataPublisher
from Utils.Infrastructure.DataProtocols.MQTT.MqttDataProtocol import MqttDataProtocol
from Utils.Settings import Config


class MqttDataPublisher(DataPublisher):

    def __init__(self, topic):
        DataPublisher.__init__(self, MqttDataProtocol)
        self.topic = topic

    def publish(self, message):

        self.publisher.send_image(self.protocol.encodeMessage(message))
