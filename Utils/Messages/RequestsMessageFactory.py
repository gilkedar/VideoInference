from Utils.Helpers.Singleton import Singleton
from Utils.Messages.Requests.ImageRequestMessage import ImageRequestMessage


class RequestsMessageFactory(metaclass=Singleton):

    request_id = 0

    def __init__(self):
        pass

    @staticmethod
    def createImageRequest(image,algorithm_name):
        RequestsMessageFactory.request_id += 1
        request_id = RequestsMessageFactory.request_id
        return ImageRequestMessage(request_id,algorithm_name, image)


