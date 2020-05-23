from Utils.Infrastructure.ImageProtocols.ImageSubscriber import ImageSubscriber
from Utils.Infrastructure.ImageProtocols.ZMQ.ZmqImageProtocol import ZmqImageProtocol
import imagezmq
import threading

class ZmqImageSubscriber(ImageSubscriber):

    def __init__(self, ip, callback_function,queue=10):
        ImageSubscriber.__init__(self,ZmqImageProtocol(), callback_function, queue)
        self.ip = ip
        self.imageHub = imagezmq.ImageHub(open_port="tcp://{}:5555".format(self.ip), REQ_REP=False)

    def subscribe(self):
        self.listen_flag = True

        while self.listen_flag:

            (text, image) = self.imageHub.recv_image()
            msg = self.protocol.decodeMessage(text, image)
            threading.Thread(target=self.callback_function, args=(msg, )).start()
