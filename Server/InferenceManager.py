from Utils.Algorithms.AlgorithmFactory import AlgorithmFactory
from Utils.Settings import Config
from Utils.Helpers.Logger import Logger
import os


class InferenceManager:

    factory = AlgorithmFactory()

    def __init__(self, algorithm_name):
        self.working_dir = os.getcwd().split("/")
        self.project_path = "/".join(self.working_dir[:-1])  # server working dir is 1 layer inside project dir
        self.algorithm_name = algorithm_name
        self.algorithm = InferenceManager.factory.createAlgorithm(self.algorithm_name)
        self.logger = Logger(self.__class__.__name__)
        self.loadAlgorithm()

    def loadAlgorithm(self):
        self.algorithm.loadModel()

    def getInference(self, input_message):
        ans = self.algorithm.run(input_message)
        return ans

    def getAlgorithm(self):
        return self.algorithm