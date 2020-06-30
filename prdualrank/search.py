"""
    Patterns search functions, includeing:
        :class Extractor
            :method fromTuple2Pattern -> bootstraping patterns from tuples
            :method fromPattern2Tuple ->  bootstraping tuples from patterns
"""
from .object import Docs, Pattern, Tuple
from .utils import isLine
            

class BasiceExtractor:
    
    # ------------------------------------------
    def __init__(self):
        self._name = "basic extractor"
    
    def fromSpan2Phrase(self, 
                        matches, 
                        left_tuple_len,
                        right_tuple_len,
                        tuple,
                        outer=2, 
                        inner=2):
        """
        separate span object into two phrase
        """
        left = left_tuple_len
        right= right_tuple_len
        phrases = []
        for span in matches:
            s_inner = inner if (len(span) - left - right - 2*inner) > 0 else (len(span) - left - right)//2
            l_outer = r_outer = outer
            while l_outer >= 0:
                phrase_left = span.doc[span.start-l_outer:span.start+left+inner]
                if isLine(phrase_left):
                    break
                l_outer -= 1
            assert l_outer >= 0
            phrase_l = (phrase_left[:l_outer], phrase_left[l_outer+left:])
            while r_outer >= 0:
                phrase_right = span.doc[span.end - inner - right:span.end+r_outer]
                if isLine(phrase_right):
                    break
                r_outer -= 1
            assert r_outer >= 0
            phrase_r = (phrase_right[:inner], phrase_right[inner+right:])
            
            phrases.append(Pattern(phrase_l, phrase_r))
        return phrases
    
    def fromPhrase2Pattern(self, phrases):
        """
        replace tuple in phrase into pattern
        """
        for phrase_left, phrase_right, l_outer, r_outer in phrases:
            pass
    
    def fromTuple2Pattern(self, tuples):
        """
        :param tuples -> [(E1, E2), (E1,E2)...]
        :return:
            patterns
            relations
        """
        raise NotImplementedError
    
    def fromPattern2Tuple(self, patterns):
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