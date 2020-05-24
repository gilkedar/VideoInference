from Utils.Helpers.Timers.MessageTimer import MessageTimer


class InferenceMessageTimer(MessageTimer):

    def __init__(self, request_id, algorithm):
        MessageTimer.__init__(self,request_id)
        self.algorithm = algorithm


    def __str__(self):
        return "{}   ({})".format(MessageTimer.__str__(self), self.algorithm)
