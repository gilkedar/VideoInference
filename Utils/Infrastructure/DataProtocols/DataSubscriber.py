from Utils.Infrastructure.Subscriber import Subscriber


class DataSubscriber(Subscriber):

    def __init__(self, protocol, callback_function, queue):
        Subscriber.__init__(self, protocol, callback_function, queue)
