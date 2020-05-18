
from Utils.Messages.Message import Message

class ResponsetMessage(Message):

    def __init__(self, request_id, ans):
        Message.__init__(self)
        self.request_id = request_id
        self.ans = ans
