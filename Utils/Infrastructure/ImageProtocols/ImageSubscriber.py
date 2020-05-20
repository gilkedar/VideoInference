from Utils.Infrastructure.Subscriber import Subscriber


class ImageSubscriber(Subscriber):

    def __init__(self, protocol, callback_function, queue):
        Subscriber.__init__(self,protocol, callback_function, queue)
