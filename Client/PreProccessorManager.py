
from Utils.Settings import Config

import cv2
import numpy as np
# from keras.preprocessing.image import img_to_array


class PreProcessorManager:

    def __init__(self):
        pass
    
    @staticmethod
    def preProcessIsSantaInput(input):
        image = cv2.resize(input, (28, 28))
        image = image.astype("float") / 255.0
        # image = img_to_array(image)
        image = np.expand_dims(image, axis=0)
        return image
    
    @staticmethod
    def PreProcessAlgorithmInput(algo_name, input):
        if algo_name == Config.ALGORITHM_IS_SANTA:
            return PreProcessorManager.preProcessIsSantaInput(input)
        else:
            return input



