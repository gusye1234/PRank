"""
    Patterns search functions, includeing:
        :class Extractor
            :method fromT2P -> bootstraping patterns from tuples
            :method fromP2T ->  bootstraping tuples from patterns
"""

class BasiceExtractor:
    def __init__(self):
        self._name = "basic extractor"
    
    def fromT2P(self, tuples):
        pass
    
    def fromP2T(self, patterns):
        pass