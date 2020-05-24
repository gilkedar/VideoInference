from Utils.Messages.Message import Message


class RequestMessage(Message):

    def __init__(self, request_id, algorithm, data):
        Message.__init__(self)
        self.request_id = request_id
        self.algorithm = algorithm
        self.data = data



