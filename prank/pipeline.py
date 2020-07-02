"""
A simple way to use tor from end to end
"""
from .world import *
from . import object
from . import rank
from . import utils
from . import search
from . import inference


class PRDualRank:
    def __init__(self, 
                 file, 
                 preload=None):
        self._file = file
        self.docs = object.Docs(file)
        self.inferor = inference.PRDualRank()
        self.docs.initialize(preload=preload)
        self.searcher = search.PRDualRankSearch(self.docs)
        
    def set_seed(self, 
                 seeds : list):
        for seed in seeds:
            object.Tuple(seed[0], seed[1], seed=True)
            
    def bootstrap(self, iter_times = 3):
        for _ in range(iter_times):
            # TODO