from Utils.Infrastructure.ImageProtocols.ImageProtocol import ImageProtocol
from Utils.Messages.Requests.ImageRequestMessage import ImageRequestMessage
from Utils.Messages.Responses.ImageResponseMessage import ImageResponseMessage

import json
import cv2
import numpy as np


class HttpImageProtocol(ImageProtocol):

    field_request_id = "HTTP_REQUEST_ID"
    field_algorithm = "HTTP_ALGORITHM"

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

        # frame = imutils.resize(image_request.data, width=128)
        # _, img_encoded = cv2.imencode('.jpg', frame)
        # # send http request with image and receive response.
        #
        # text = "{}{}{}".format(image_request.request_id, self.DATA_SEPARATOR, image_request.algorithm, self.DATA_SEPARATOR)

        ans = {}
        ans[self.field_request_id] = image_request.request_id
        ans[self.field_algorithm] = image_request.algorithm
        # ans[self.field_image] = image_request.data.tolist()
        return json.dumps(ans)

    def decodeMessage(self, input_msg):
        """

        :param text: request id and algorithm in one string
        :param image: open CV instance of an image
        :return: ImageRequestMessage
        """
        request_id = input_msg.headers.environ[self.field_request_id]
        algorithm = input_msg.headers.environ[self.field_algorithm]
        img_str = input_msg.data
        tmp_img = np.frombuffer(img_str, np.uint8)
        image = cv2.imdecode(tmp_img, flags=1)
        # do some fancy processing here....
        return ImageRequestMessage(request_id, algorithm, image)


