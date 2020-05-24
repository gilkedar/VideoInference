from Utils.Messages.Responses.ResponseMessage import ResponseMessage


class ImageResponseMessage(ResponseMessage):

    def __init__(self, request_id, algorithm, ans):
        ResponseMessage.__init__(self, request_id=request_id, algorithm=algorithm, ans=ans)
