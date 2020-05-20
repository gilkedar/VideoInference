from Utils.Infrastructure.ImageProtocols.ImageSubscriber import ImageSubscriber
from Utils.Infrastructure.ImageProtocols.ZMQ.ZmqImageProtocol import ZmqImageProtocol
import imagezmq
import threading

class ZmqImageSubscriber(ImageSubscriber):

    def __init__(self, callback_function,queue=10):
        ImageSubscriber.__init__(self,ZmqImageProtocol, callback_function,queue)
        self.imageHub = imagezmq.ImageHub()

    def subscribe(self):
        self.listen_flag = True

        while self.listen_flag:

            (text, image) = self.imageHub.recv_image()
            msg = self.protocol.decodeMessage(text, image)
            print(msg)
            threading.Thread(self.callback_function, args=(msg, )).start()
