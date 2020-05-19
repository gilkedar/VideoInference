from Utils.Messages.Requests.RequestMessage import RequestMessage


class ImageRequestMessage(RequestMessage):

    def __init__(self, request_id, algorithm, image):
        RequestMessage.__init__(self, request_id, algorithm, image)
