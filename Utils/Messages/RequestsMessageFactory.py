from Utils.Helpers.Singleton import Singleton
from Utils.Messages.Requests.RequestMessage import RequestMessage
from Utils.Settings import Config


class RequestsMessageFactory(metaclass=Singleton):

    message_id = 0

    def __init__(self):
        pass

    @staticmethod
    def createRequest(image,algorithm_name):
        RequestsMessageFactory.message_id += 1
        request_id = RequestsMessageFactory.message_id
        return RequestMessage(request_id,image,algorithm_name)


