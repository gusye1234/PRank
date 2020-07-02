"""
    Patterns search functions, includeing:
        :class Extractor
            :method fromTuple2Pattern -> bootstrapping patterns from tuples
            :method fromPattern2Tuple ->  bootstrapping tuples from patterns
"""
from .world import *
from .object import Docs, Pattern, Tuple
from .utils import * 
            

class BasiceExtractor:
    
    # ------------------------------------------
    def __init__(self):
        self._name = "basic extractor"
    
    @staticmethod
    def fromSpan2Pattern(matches, 
                        tuple : Tuple,
                        outer, 
                        inner):
        """
        separate span object into two phrase
        """
        left = len(tuple[0])
        right= len(tuple[1])
        patterns = []
        for span in matches:
            s_inner = inner if (len(span) - left - right - 2*inner) >= 0 else (len(span) - left - right)//2
            l_outer = r_outer = outer
            while l_outer >= 0:
                if span.start-l_outer < 0:
                    l_outer -= 1
                    continue
                phrase_left = span.doc[span.start-l_outer:span.start+left+s_inner]
                if isLine(phrase_left):
                    break
                l_outer -= 1
            if l_outer < 0:
                continue
            phrase_l = (phrase_left[:l_outer], phrase_left[l_outer+left:])
            while r_outer >= 0:
                phrase_right = span.doc[span.end - s_inner - right:span.end+r_outer]
                if isLine(phrase_right):
                    break
                r_outer -= 1
            if r_outer < 0:
                continue
            phrase_r = (phrase_right[:s_inner], phrase_right[s_inner+right:])
            # print(phrase_l, phrase_r)
            new_found = Pattern(phrase_l, phrase_r)
            tuple.relate(new_found)
            patterns.append(new_found)
        return patterns
    
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
    def __init__(self, 
                 docs : Docs):
        super(PRDualRankSearch, self).__init__()
        self._name = "prdualrank sampler"
        self.docs = docs
        self.pat_iter_times = 0
        self.tup_iter_times = 0
    
    def fromTuple2Pattern(self, tuples, outer=1, inner=2):
        self.pat_iter_times += 1
        # patterns = set([])
        
        for tup in track(tuples, description=f"    ({self.pat_iter_times}) Q:patterns"):
            phrase_left = span2low(tup[0])
            phrase_right = span2low(tup[1])
            tuple_search = generate_wildcard(phrase_left, phrase_right, cards=MAX_RELATION)
            matches = self.docs.match(tuple_search)
            # print(matches)
            # patterns.update(self.fromSpan2Pattern(matches, tup, outer, inner))
            self.fromSpan2Pattern(matches, tup, outer, inner)
        
        # return patterns
    
    
    def fromPattern2Tuple(self, patterns, tuples):
        """
        TODO
        """
        self.tup_iter_times += 1
        # new_tuples = set([])
        for tup in track(tuples, description=f"    ({self.tup_iter_times}) Q:tuples"):
            tup : Tuple
            # attribute search
            for pat in patterns:
                pat : Pattern
                e1 = pat.attribute_pattern(tup, left=True)
                e2 = pat.attribute_pattern(tup, left=False)
                e1_matches = self.docs.match(e1)
                e2_matches = self.docs.match(e2)
                new_tup = [pat.getTuple(match) for match in e1_matches] + [pat.getTuple(match) for match in e2_matches]
                [tup.relate(pat) for tup in new_tup]
                # new_tuples.update(
                #     new_tup
                # )
        # return new_tuples
                