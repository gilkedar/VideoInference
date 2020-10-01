from Utils.Messages.Requests.RequestMessage import RequestMessage


class ImageRequestMessage(RequestMessage):

    def __init__(self, request_id, algorithm, image):
        RequestMessage.__init__(self, request_id, algorithm, image)
        self.original_width, self.original_height, _ = image.shape

    def getOriginalImageShape(self):
        return (self.original_width, self.original_height)