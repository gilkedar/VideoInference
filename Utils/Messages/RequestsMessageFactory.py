from Utils.Helpers.Singleton import Singleton
from Utils.Messages.Requests.ImageRequestMessage import ImageRequestMessage


class RequestsMessageFactory(metaclass=Singleton):

    def __init__(self):
        pass

    @staticmethod
    def createImageRequest(image_id, image, algorithm_name):
        return ImageRequestMessage(image_id, algorithm_name, image)


