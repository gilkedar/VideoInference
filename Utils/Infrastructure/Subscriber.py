

class Subscriber:

    def __init__(self, protocol, callback_function, queue):
        self.protocol = protocol
        self.callback_function = callback_function
        self.queue = queue

        self.listen_flag = False

    def subscribe(self):
        pass

    def stopListening(self):
        self.listen_flag = False
