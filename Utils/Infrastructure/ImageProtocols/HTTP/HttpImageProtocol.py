from Utils.Infrastructure.ImageProtocols.ImageProtocol import ImageProtocol
from Utils.Messages.Requests.ImageRequestMessage import ImageRequestMessage


class HttpImageProtocol(ImageProtocol):

    def __init__(self):
        ImageProtocol.__init__(self)
        pass

    def encodeMessage(self, image_request):
        """
        encode the desired image request message to fit the zmq pub/sub protocol
        :param image_request: ImageRequestMessage to be encdoded

        :return: (text, image) tuple
        """
        pass

    def decodeMessage(self, text, image):
        """
        :param text: request id and algorithm in one string
        :param image: open CV instance of an image
        :return: ImageRequestMessage
        """
        request_id, algorithm = None,None
        return ImageRequestMessage(request_id, algorithm, image)
