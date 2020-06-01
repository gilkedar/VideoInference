from Utils.Algorithms.Algorithm import Algorithm
from Utils.Algorithms.AlgorithmResponses.IsSantaResponse import IsSantaResponseMessage

from Utils.Settings import Config

from keras.models import load_model
import numpy as np


class IsSantaAlgorithm(Algorithm):

    def __init__(self, model_path):
        Algorithm.__init__(self, name=Config.ALGORITHM_IS_SANTA, model_path=model_path)

    def loadModel(self):
        self.model = load_model(self.model_path)

    def run(self, input_image):

        image = np.array(input_image)

        with self.model_lock:
            # classify the input image
            (not_santa_prob, santa_prob) = self.model.predict(image)[0]

        # build the label
        is_santa_ans = True if santa_prob > not_santa_prob else False

        ans = IsSantaResponseMessage(is_santa_ans, santa_prob, not_santa_prob)
        return ans

