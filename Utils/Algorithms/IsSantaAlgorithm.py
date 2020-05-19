from Utils.Algorithms.Algorithm import Algorithm

from Utils.Settings import Config

class IsSantaAlgorithm(Algorithm):

    def __init__(self, model_path):
        Algorithm.__init__(self, name=Config.ALGORITHM_IS_SANTA, model_path=model_path)

    def run(self, model_input):
        ans = True  # @TODO - run true prediction for image
        return ans
