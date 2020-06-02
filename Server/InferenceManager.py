from Utils.Algorithms.DetectFacesAlgorithm import DetectFacesAlgorithm
from Utils.Algorithms.DetectObjectsAlgorithm import DetectObjectsAlgorithm
from Utils.Algorithms.IsSantaAlgorithm import IsSantaAlgorithm
from Utils.Algorithms.Algorithm import Algorithm
from Utils.Settings import Config
from Utils.Helpers.Logger import Logger
import os


class InferenceManager:

    def __init__(self):
        # extrace the VideoInference Project directory
        self.working_dir = os.getcwd().split("/")
        self.project_path = "/".join(self.working_dir[:-1])  # server working dir is 1 layer inside project dir

        self.is_santa_algorithm = IsSantaAlgorithm(self.project_path + Config.MODEL_PATH_IS_SANTA_ALGORITHM)
        self.detect_faces_algorithm = DetectFacesAlgorithm(self.project_path + Config.MODEL_PATH_DETECT_FACES_ALGORITHM,
                                                           self.project_path + Config.MODEL_PATH_DETECT_FACES_PROTOTEXT_ALGORITHM)

        self.logger = Logger(self.__class__.__name__)
        self.loadAlgorithms()

    @staticmethod
    def loadAlgorithms():
        for algo in Algorithm.possible_algorithms:
            algo.loadModel()

    @staticmethod
    def getAlgorithmInstanceFromName(algorithm_name):

        for algo in Algorithm.possible_algorithms:
            if algo.name == algorithm_name:
                return algo

    @staticmethod
    def getInference(algorithm_name, input_message):

        algorithm = InferenceManager.getAlgorithmInstanceFromName(algorithm_name)
        ans = algorithm.run(input_message)
        return ans
