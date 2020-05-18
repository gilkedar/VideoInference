import imagezmq
from Utils.Protocols.ImageProtocol import ImageProtocol

class ZmqSubscriber(ImageProtocol):

    def __init__(self):
        ImageProtocol.__init__(self)
        self.imageHub = imagezmq.ImageHub()

    def subscribe(self):
        while True:

            (msg, frame) = self.imageHub.recv_image()
            print(msg)
