
from Utils.Messages.Message import Message

class RequestMessage(Message):

    def __init__(self,id,algorithm, data):
        Message.__init__(self)
        self.request_id = id
        self.algorithm = algorithm
        self.data = data

        self.request_start_time = None
        self.request_end_time = None

