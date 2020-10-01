
from Utils.Algorithms.IsSantaAlgorithm import IsSantaAlgorithm
from Utils.Algorithms.DetectFacesAlgorithm import DetectFacesAlgorithm
from Utils.Algorithms.DetectObjectsAlgorithm import DetectObjectsAlgorithm
from Utils.Helpers.Singleton import Singleton
from Utils.Settings import Config


class AlgorithmFactory(metaclass=Singleton):

    def __init__(self):
        pass

    @staticmethod
    def createAlgorithm(algorithm_name):
        if algorithm_name == Config.ALGORITHM_IS_SANTA:
            return IsSantaAlgorithm(Config.MODEL_PATH_IS_SANTA_ALGORITHM)
        elif algorithm_name == Config.ALGORITHM_DETECT_FACES:
            return DetectFacesAlgorithm(Config.MODEL_PATH_DETECT_FACES_ALGORITHM,
                                        Config.MODEL_PATH_DETECT_FACES_PROTOTEXT_ALGORITHM)
        else:
            return None


