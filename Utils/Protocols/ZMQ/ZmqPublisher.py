import imagezmq
import socket
from Utils.Settings import Config


class ZmqPublisher:

    def __init__(self, ip, port=Config.ZMQ_DEFAULT_PORT):
        self.ip = ip
        self.port = port

        self.sender = imagezmq.ImageSender(connect_to="tcp://{}:{}}".format(ip, port), REQ_REP=False)

    def publish(self,message):
        text = "{}{}{}".format(message.request_id,Config.MESSAGE_SEPARATOR,message.algorithm_name)
        self.sender.send_image(text, message.image)
