
from Utils.Settings import Config

import cv2
import numpy as np


class PreProcessorManager:

    def __init__(self):
        pass

    @staticmethod
    def prePricessDetectFacesInput(input_image):
        resized = cv2.resize(input_image, (300, 300))
        return np.array(resized, dtype=np.uint8)

    @staticmethod
    def preProcessIsSantaInput(input_image):
        image = cv2.resize(input_image, (28, 28))
        image = image.astype("float") / 255.0
        # image = img_to_array(image)
        image = np.expand_dims(image, axis=0)
        return image
    
    @staticmethod
    def PreProcessAlgorithmInput(algo_name, input_image):
        if algo_name == Config.ALGORITHM_IS_SANTA:
            return PreProcessorManager.preProcessIsSantaInput(input_image)
        elif algo_name == Config.ALGORITHM_DETECT_FACES:
            return PreProcessorManager.prePricessDetectFacesInput(input_image)
        else:
            return input_image



