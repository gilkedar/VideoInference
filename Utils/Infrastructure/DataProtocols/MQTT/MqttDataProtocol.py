
from Utils.Infrastructure.DataProtocols.DataProtocol import DataProtocol
from Utils.Messages.Responses.ImageResponseMessage import ImageResponseMessage
from Utils.Settings import Config
import json

class MqttDataProtocol(DataProtocol):

    field_request_id = "request_id"
    field_algorithm = "algorithm"
    field_ans = "ans"

    def __init__(self):
        DataProtocol.__init__(self)
        pass


    def encodeMessage(self ,image_response):
        """
        encode the image response message to mqqt msg type
        :param image_response: ImageRequestMessage to be encdoded

        :return: json string of the answer message
        """
        msg = {}
        msg[self.field_request_id] = image_response.request_id
        msg[self.field_algorithm] = image_response.algorithm
        msg[self.field_ans] = image_response.ans

        return json.dumps(msg)

    def decodeMessage(self, message_json):
        """

        :param text: request id and algorithm in one string
        :param image: open CV instance of an image
        :return: ImageRequestMessage
        """
        msg = json.loads(message_json)
        request_id = msg[self.field_request_id]
        algorithm = msg[self.field_algorithm]
        ans = msg[self.field_ans]

        msg = ImageResponseMessage(request_id, algorithm, ans)
        return msg