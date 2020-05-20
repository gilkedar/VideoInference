from Utils.Infrastructure.ImageProtocols.ImagePublisher import ImagePublisher
from Utils.Infrastructure.ImageProtocols.HTTP.HttpImageProtocol import HttpImageProtocol
from Utils.Settings import Config

class HttpImagePublisher(ImagePublisher):

    def __init__(self, ip, port=80):
        ImagePublisher.__init__(self,HttpImageProtocol)
        self.ip = ip
        self.port = port

    def publish(self,message):
        pass