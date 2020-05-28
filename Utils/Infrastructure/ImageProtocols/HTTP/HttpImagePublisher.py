from Utils.Infrastructure.ImageProtocols.ImagePublisher import ImagePublisher
from Utils.Infrastructure.ImageProtocols.HTTP.HttpImageProtocol import HttpImageProtocol
from Utils.Settings import Config
import requests
import json


class HttpImagePublisher(ImagePublisher):

    def __init__(self, ip, port=Config.HTTP_PORT, api=""):
        ImagePublisher.__init__(self,HttpImageProtocol())
        self.ip = ip
        self.port = port
        self.api = api

    def publish(self,message):
        address = 'http://{}:{}/{}'.format(self.ip, self.port, self.api)

        headers = {'content-type': 'application/json'}
        # content_type = 'image/jpeg'
        # headers = {'content-type': content_type}

        response = requests.post(address, data=self.protocol.encodeMessage(message), headers=headers)

        # decode response

        print(response.text)