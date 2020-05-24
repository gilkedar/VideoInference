from Utils.Helpers.Timers.MessageTimer import MessageTimer


class RequestMessageTimer(MessageTimer):

    def __init__(self, request_id):
        MessageTimer.__init__(self,request_id)


