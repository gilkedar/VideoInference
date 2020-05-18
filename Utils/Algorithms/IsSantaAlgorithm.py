from Utils.Algorithms.Algorithm import Algorithm
from Utils.Settings import Config

class IsSantaAlgorithm(Algorithm):

    def __init__(self):
        Algorithm.__init__(self, Config.ALGORITHM_IS_SANTA)

