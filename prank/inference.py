"""
    Inference methos to estimate Precision and Recall
        :class BasicMethod -> define a set of methods an inference class should have
        :class PRDualRank -> the original PRDualRank algorithm
"""
from .world import *
import numpy as np
import scipy.sparse as sp
from scipy.sparse import csr_matrix
from pprint import pprint
class BasicMethod:
    def __init__(self):
        self._name = 'basic inference'
        self._context = None
        self._graph = None
    
    @property
    def name(self):
        return self._name
    
    def builddict(self, tuples, patterns):
        """
        assert tuples and patterns are list-like obj
        """
        self.T2id = {}
        self.id2T = tuples
        self.P2id = {}
        self.id2P = patterns
        for i, T in enumerate(tuples):
            self.T2id[T] = i
        for i, P in enumerate(patterns):
            self.P2id[P] = i
            
    def buildgraph(self, relation : dict, ask_graph=True):
        """
        build tuple-pattern bipartite graph without any normalization.
        """
        assert len(self.id2T) == len(relation)
        n = len(self.id2T)
        m = len(self.id2P)
        if self._context is None:
            context_values = []
            context_tuples = []
            context_patterns = []
            for tup, relate in relation.items():
                id_t = self.T2id[tup]
                for pattern, value in relate.items():
                    id_p = self.P2id[pattern]
                    context_tuples.append(id_t)
                    context_patterns.append(id_p)
                    context_values.append(value)

            self._context = csr_matrix(
                (context_values, (context_tuples, context_patterns)),
                shape=(n, m)
            )
            if ask_graph:
                bigraph = sp.dok_matrix((n+m, n+m), dtype=np.float16)
                C = self._context.tolil()
                bigraph[:n, n:] = C
                bigraph[n:, :n] = C.T
                self._graph = bigraph.tocsr()
        
    def infer(self, tuples, patterns, relation):
        """
        basic methods to score tuples 
        :param: examples:
            tuples = [(1,2), (3,6), (2, 4)]
            patterns=["plus one", "* 2", "square"]
            relation = {
                tuples[0] : {patterns[0]:39, patterns[1] : 1},
                tuples[1] : {patterns[1] : 40},
                tuples[2] : {patterns[1] : 20, patterns[2] : 20},
            }
        """
        raise NotImplementedError(f"infer methods of {self.name} is not implemented")
    


class PRDualRank(BasicMethod):
    def __init__(self):
        super(PRDualRank, self).__init__()
        self._name = "prdualrank"
    
    def _normalization(self):
        degree = np.array(self._context.sum(axis=1))
        column = np.array(self._context.sum(axis=0))
        degree[degree<= 1e-7] = 1.
        column[column<= 1e-7] = 1.
        d_inv = np.power(degree, -1.).flatten()
        c_inv = np.power(column, -1.).flatten()
        d_mat = sp.diags(d_inv)
        c_mat = sp.diags(c_inv)
        Cr = d_mat.dot(self._context).tocsr()
        Cc = self._context.dot(c_mat).tocsr()
        if self._graph is not None:
            d = np.array(self._graph.sum(axis=1))
            d[d==0.] = 1.
            d_inv = np.power(d, -1.).flatten()
            d_mat = sp.diags(d_inv)
            self.P = d_mat.dot(self._graph)
            self.R = self.P.T
        return Cr, Cc
    
    def infer(self, 
              tuples : list, 
              patterns : list,
              relation : dict,
              seed_tuples = None,
              max_iter = 100,
              delta = 1e-5):
        """
        Infer precision and recall using PRDualRank
            :param 
        """
        self.builddict(tuples, patterns)
        self.buildgraph(relation, ask_graph=False) 
        Cr, Cc = self._normalization()
        CrT = Cr.T
        CcT = Cc.T
        n = len(tuples)
        m = len(patterns)
        precision = np.zeros(n+m)
        recall = np.zeros(n+m)
        seed_id = [self.T2id[tup] for tup in seed_tuples]
        precision[seed_id] = 1.
        recall[seed_id] = 1/len(seed_id)
        
        for i in track(range(max_iter), description="PRDualRank infering"):
            precision[n:] = CcT.dot(precision[:n])
            precision[:n] = Cr.dot(precision[n:])
            precision[seed_id] = 1.
            recall[n:] = CrT.dot(recall[:n])
            recall[:n] = Cc.dot(recall[n:])
        return {
            'tuple precision' : precision[:n],
            'pattern precision' : precision[n:],
            'tuple recall' : recall[:n],
            'pattern recall': recall[n:]
        }
    