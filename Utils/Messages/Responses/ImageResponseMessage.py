from Utils.Messages.Responses.ResponseMessage import ResponsetMessage


class ImageResponseMessage(ResponsetMessage):

    def __init__(self, request_id, algorithm, ans):
        ResponsetMessage.__init__(self, request_id=request_id, algorithm=algorithm, ans=ans)
