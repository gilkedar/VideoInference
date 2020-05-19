
from Utils.Infrastructure.DataProtocols.DataProtocol import DataProtocol
from Utils.Messages.Responses.ImageResponseMessage import ImageResponseMessage
from Utils.Settings import Config

class MqttDataProtocol(DataProtocol):


    def __init__(self):
        DataProtocol.__init__(self)
        pass


    def encodeMessage(self ,image_response):
        """
        encode the image response message to mqqt msg type
        :param image_response: ImageRequestMessage to be encdoded

        :return: json string of the answer message
        """
        pass

    def decodeMessage(self, message_json):
        """

        :param text: request id and algorithm in one string
        :param image: open CV instance of an image
        :return: ImageRequestMessage
        """
        request_id = message_json.request_id
        algorithm = message_json.algorithm
        ans = message_json.ans
        return ImageResponseMessage(request_id, algorithm, ans)
