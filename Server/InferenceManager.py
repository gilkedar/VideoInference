from Utils.Algorithms.DetectFacesAlgorithm import DetectFacesAlgorithm
from Utils.Algorithms.DetectObjectsAlgorithm import DetectObjectsAlgorithm
from Utils.Algorithms.IsSantaAlgorithm import IsSantaAlgorithm
from Utils.Algorithms.Algorithm import Algorithm
from Utils.Settings import Config
from Utils.Helpers.Logger import Logger


class InferenceManager:

    def __init__(self):

        self.is_santa_algorithm = IsSantaAlgorithm(Config.MODEL_PATH_IS_SANTA_ALGORITHM)

        self.logger = Logger(self.__class__.__name__)

    @staticmethod
    def loadAlgorithms():
        for algo in Algorithm.possible_algorithms:
            algo.loadModel()

    def getAlgorithmInstanceFromName(self,algorithm_name):

        for algo in Algorithm.possible_algorithms:
            if algo.name == algorithm_name:
                return algo

    def getInference(self,algorithm_name, input_message):

        algorithm = self.getAlgorithmInstanceFromName(algorithm_name)
        ans = algorithm.run(input_message)
        return ans



