import threading

class Publisher:

    def __init__(self, protocol):
        self.protocol = protocol
        self.publisher = None
        self.lock = threading.Lock()

    def publish(self, message):
        pass