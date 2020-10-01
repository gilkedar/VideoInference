from Utils.Messages.Responses.ResponseMessage import ResponseMessage


class ImageResponseMessage(ResponseMessage):

    def __init__(self, request_id, algorithm, ans, updated_frame):
        ResponseMessage.__init__(self, request_id=request_id, algorithm=algorithm, ans=ans)
        self.updated_frame = updated_frame
