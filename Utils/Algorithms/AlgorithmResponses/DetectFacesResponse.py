
from Utils.Settings import Config
import json

class DetectFacesResponse:

    field_boxes = "face_boxes"
    field_probabilities = "probabilities"

    def __init__(self, request_id, boxes, probabilities):
        self.request_id = request_id
        self.boxes = boxes
        self.probabilities = probabilities

    def serialize(self):
        dic = dict()
        dic[self.field_boxes] = [list(int(x) for x in tup) for tup in self.boxes]
        dic[self.field_probabilities] = [str(x) for x in self.probabilities]
        return dic

    @staticmethod
    def getBoxesAndLabels(response_dic):
        probabilities = response_dic[DetectFacesResponse.field_probabilities]
        boxes = response_dic[DetectFacesResponse.field_boxes]
        labels = []

        for probability in probabilities:
            # draw the bounding box of the face along with the associated
            label = "{:.3f}%".format( float(probability) * 100)
            labels.append(label)

        return boxes, labels

