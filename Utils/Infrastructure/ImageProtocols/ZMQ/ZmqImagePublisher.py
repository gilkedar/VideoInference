from Utils.Infrastructure.ImageProtocols.ImagePublisher import ImagePublisher
from Utils.Infrastructure.ImageProtocols.ZMQ.ZmqImageProtocol import ZmqImageProtocol
from Utils.Settings import Config

import imagezmq


class ZmqImagePublisher(ImagePublisher):

    def __init__(self, ip=Config.LOCALHOST_IP, port=Config.ZMQ_PORT, req_rep=False, tcp_udp="tcp"):
        ImagePublisher.__init__(self, ZmqImageProtocol())
        self.ip = ip
        self.port = port
        self.address = "{}://{}:{}".format(tcp_udp, ip, port)
        self.req_rep = req_rep
        self.tcp_udp = tcp_udp
        self.publisher = imagezmq.ImageSender(connect_to=self.address, REQ_REP=req_rep)

    def publish(self, message):
        with self.lock:
            text, image = self.protocol.encodeMessage(message)
            self.publisher.send_image(text, image)