from Utils.Infrastructure.ImageProtocols.ImageSubscriber import ImageSubscriber
from Utils.Infrastructure.ImageProtocols.ZMQ.ZmqImageProtocol import ZmqImageProtocol
from Utils.Settings import Config
import imagezmq
import threading

class ZmqImageSubscriber(ImageSubscriber):

    def __init__(self, ip,callback_function, port=Config.ZMQ_PORT, queue=10):
        ImageSubscriber.__init__(self,ZmqImageProtocol(), callback_function, queue)
        self.ip = ip
        self.port = port
        self.imageHub = imagezmq.ImageHub(open_port="tcp://{}:{}".format(self.ip, self.port), REQ_REP=False)

    def subscribe(self):
        self.listen_flag = True

        while self.listen_flag:

            (text, image) = self.imageHub.recv_image()
            msg = self.protocol.decodeMessage(text, image)
            threading.Thread(target=self.callback_function, args=(msg, )).start()

