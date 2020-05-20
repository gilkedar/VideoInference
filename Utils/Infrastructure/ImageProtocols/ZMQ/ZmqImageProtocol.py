from Utils.Infrastructure.ImageProtocols.ImageProtocol import ImageProtocol
from Utils.Messages.Requests.ImageRequestMessage import ImageRequestMessage
from Utils.Settings import Config

class ZmqImageProtocol(ImageProtocol):

    TEXT_SEPARATOR = "-"

    def __init__(self):
        ImageProtocol.__init__(self)
        pass


    def encodeMessage(self,image_request):
        """
        encode the desired image request message to fit the zmq pub/sub protocol
        :param image_request: ImageRequestMessage to be encdoded

        :return: (text, image) tuple
        """
        return

    def decodeMessage(self, text, image):
        """

        :param text: request id and algorithm in one string
        :param image: open CV instance of an image
        :return: ImageRequestMessage
        """
        request_id, algorithm = text.split(ZmqImageProtocol.TEXT_SEPARATOR)
        return ImageRequestMessage(request_id, algorithm,image)
