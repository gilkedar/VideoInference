from Utils.Infrastructure.ImageProtocols.ImageProtocol import ImageProtocol
from Utils.Messages.Requests.ImageRequestMessage import ImageRequestMessage
#import cv2
import json
import imutils

class HttpImageProtocol(ImageProtocol):

    field_request_id = "request_id"
    field_algorithm = "algorithm"
    field_image = "image_data"

    def __init__(self):
        ImageProtocol.__init__(self)
        pass

    def encodeMessage(self, image_request):
        """
        encode the desired image request message to fit the zmq pub/sub protocol
        :param image_request: ImageRequestMessage to be encdoded

        :return: (text, image) tuple
        """
        # img = image_request.data
        # # encode image as jpeg
        frame = imutils.resize(image_request.data, width=128)
        # _, img_encoded = cv2.imencode('.jpg', frame)
        # # send http request with image and receive response.
        #
        # text = "{}{}{}".format(image_request.request_id, self.DATA_SEPARATOR, image_request.algorithm, self.DATA_SEPARATOR)

        ans = {}
        ans[self.field_request_id] = image_request.request_id
        ans[self.field_algorithm] = image_request.algorithm
        # ans[self.field_image] = image_request.data.tolist()
        ans[self.field_image] = frame.tolist()
        return json.dumps(ans)

    def decodeMessage(self, input_msg):
        """

        :param text: request id and algorithm in one string
        :param image: open CV instance of an image
        :return: ImageRequestMessage
        """
        image_request = json.loads(input_msg.data)
        request_id = image_request[self.field_request_id]
        algorithm = image_request[self.field_algorithm]
        image = image_request[self.field_image]
        # do some fancy processing here....
        return ImageRequestMessage(request_id, algorithm, image)

    def decodeResponse(self, request):
        return "1-2-3"
