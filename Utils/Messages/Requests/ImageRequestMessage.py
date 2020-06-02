from Utils.Messages.Requests.RequestMessage import RequestMessage


class ImageRequestMessage(RequestMessage):

    def __init__(self, request_id, algorithm, image, original_image_shape):
        RequestMessage.__init__(self, request_id, algorithm, image)
        self.original_width, self.original_height = original_image_shape

    def getOriginalImageShape(self):
        return (self.original_width, self.original_height)