
from Utils.Messages.Message import Message

class RequestMessage(Message):

    def __init__(self,id,image,algorithm):
        Message.__init__(self)
        self.request_id = id
        self.image = image
        self.algorithm = algorithm
