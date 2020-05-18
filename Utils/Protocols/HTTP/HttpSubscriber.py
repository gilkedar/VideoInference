
from Utils.Protocols.ImageProtocol import ImageProtocol

class HttpSubscriber(ImageProtocol):

    def __init__(self):
        ImageProtocol.__init__(self)
        # self.imageHub = imagezmq.ImageHub()
        pass

    def subscribe(self):
        while True:

            # (msg, frame) = self.imageHub.recv_image()
            pass