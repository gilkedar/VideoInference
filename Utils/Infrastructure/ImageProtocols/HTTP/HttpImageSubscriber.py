from Utils.Infrastructure.ImageProtocols.ImageSubscriber import ImageSubscriber
from Utils.Infrastructure.ImageProtocols.HTTP.HttpImageProtocol import HttpImageProtocol

import threading


class HttpImageSubscriber(ImageSubscriber):

    def __init__(self, callback_function, queue=10):
        ImageSubscriber.__init__(self, HttpImageProtocol, callback_function, queue)

    def subscribe(self):
        self.listen_flag = True

        while self.listen_flag:
            (text, image) = None, None
            msg = self.protocol.decodeMessage(text, image)
            print(msg)
            threading.Thread(self.callback_function, args=(msg,)).start()
