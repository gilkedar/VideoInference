
class ImageProtocol:

    def __init__(self):
        self.callback_function = None

    def setCallbackFunction(self,func):
        self.callback_function = func

    def inputToMessage(self):
        pass
