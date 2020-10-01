import json

class Message:

    def __init__(self):
        # self.message_id = 0
        # self.send_time = None
        # self.receive_time = None
        pass

    def setMessageId(self):
        pass

    def toJSON(self):
        return json.dumps(self.__dict__)
