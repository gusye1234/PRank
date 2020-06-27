"""
    Inference methos to estimate Precision and Recall
        :class BasicMethod -> define a set of methods an inference class should have
        :class PRDualRank -> the original PRDualRank algorithm
"""

class BasicMethod:
    def __init__(self):
        self._name = 'basic inference'
    
    @property
    def name(self):
        return self._name
    
    def infer(self, tuples, patterns):
        raise NotImplementedError(f"infer methods of {self.name} is not implemented")
    


class PRDualRank(BasicMethod):
    def __init__(self):
        super(self, PRDualRank).__init__()
        self._name = "prdualrank"
        