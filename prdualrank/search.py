"""
    Patterns search functions, includeing:
        :class Extractor
            :method fromT2P -> bootstraping patterns from tuples
            :method fromP2T ->  bootstraping tuples from patterns
"""
from .fileobject import Docs

class BasiceExtractor:
    
    # ------------------------------------------
    def __init__(self):
        self._name = "basic extractor"
    
    def fromT2P(self, tuples):
        """
        :param tuples -> [(E1, E2), (E1,E2)...]
        :return:
            patterns
            relations
        """
        raise NotImplementedError
    
    def fromP2T(self, patterns):
        """
        :param patterns -> [phrase1, ...]
        :return:
            tuples
            relations
        """
        raise NotImplementedError
    

class PRDualRankSearch(BasiceExtractor):
    def __init__(self):
        self._name = "prdualrank sampler"
    
    def fromT2P(self, tuples):
        pass