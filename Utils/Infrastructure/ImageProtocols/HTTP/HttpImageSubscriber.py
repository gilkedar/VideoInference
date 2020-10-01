from Utils.Infrastructure.ImageProtocols.ImageSubscriber import ImageSubscriber
from Utils.Infrastructure.ImageProtocols.HTTP.HttpImageProtocol import HttpImageProtocol


class HttpImageSubscriber(ImageSubscriber):

    def __init__(self, callback_function, queue=10):
        ImageSubscriber.__init__(self, HttpImageProtocol(), callback_function, queue)

    def subscribe(self):
        # subscribing using Flask in mainServer
        self.listen_flag = True

    def decodeIncomingRequest(self, request):
        # build a response dict to send back to client
        request_message = self.protocol.decodeMessage(request)
        return request_message
