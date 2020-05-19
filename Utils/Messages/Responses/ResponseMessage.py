
from Utils.Messages.Message import Message

class ResponsetMessage(Message):

    def __init__(self, request_id, algorithm, ans):
        Message.__init__(self)
        self.request_id = request_id
        self.algorithm = algorithm
        self.ans = ans

        self.response_start_time = None
        self.response_end_time = None
