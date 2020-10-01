from Utils.Messages.Message import Message
import json


class ResponseMessage(Message):

    def __init__(self, request_id, algorithm, ans):
        Message.__init__(self)
        self.request_id = request_id
        self.algorithm = algorithm
        self.ans = ans

