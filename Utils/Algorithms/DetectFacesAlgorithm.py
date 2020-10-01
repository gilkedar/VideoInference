from Utils.Algorithms.Algorithm import Algorithm
from Utils.Settings import Config
import cv2

from Utils.Algorithms.AlgorithmResponses.DetectFacesResponse import DetectFacesResponse

import numpy as np


class DetectFacesAlgorithm(Algorithm):

    def __init__(self, model_path, prototxt_path, min_confidence=0.3):
        Algorithm.__init__(self, name=Config.ALGORITHM_DETECT_FACES, model_path=model_path)
        self.min_confidence = min_confidence
        self.prototxt_path = prototxt_path

    def loadModel(self):
        self.model = cv2.dnn.readNetFromCaffe(self.prototxt_path, self.model_path)

    def preProcessData(self, original_frame):
        resized = cv2.resize(original_frame, (300, 300))
        return np.array(resized, dtype=np.uint8)

    def run(self, request_message):

        # image = cv2.imread("/home/gilkedar/workspace/VideoInference/Tests/ImageTestFile/person.jpeg")
        # resized_image = cv2.resize(image, (300,300))
        # blob = cv2.dnn.blobFromImage(resized_image, 1.0, (300, 300), (104.0, 177.0, 123.0))

        request_id = request_message.request_id
        image = self.preProcessData(request_message.data)
        blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300), (104.0, 177.0, 123.0))
        h, w = request_message.getOriginalImageShape()

        with self.model_lock:

            self.model.setInput(blob)
            detections = self.model.forward()

            boxes = []
            probabilities = []

            for i in range(0, detections.shape[2]):
                # extract the confidence (i.e., probability) associated with the
                # prediction
                confidence = detections[0, 0, i, 2]
                # filter out weak detections by ensuring the `confidence` is
                # greater than the minimum confidence
                if confidence > self.min_confidence:
                    # compute the (x, y)-coordinates of the bounding box for the
                    # object
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")
                    boxes.append((startX, startY, endX, endY))
                    probabilities.append(confidence)

            ans = DetectFacesResponse(request_id, boxes, probabilities)

            return ans

    def updateFrame(self, original_frame, response):
        request_id = response.request_id
        image = self.frame_editor.addFrameIdLabel(original_frame, request_id)
        boxes, labels = DetectFacesResponse.getBoxesAndLabels(response.serialize())
        return self.frame_editor.addBoxesToFrame(image, boxes, labels)