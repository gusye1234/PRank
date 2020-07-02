import spacy
from spacy.tokens.doc import Doc
from .world import *
from tqdm import tqdm
import numpy as np
import pickle
from .utils import pattern_match_backward, pattern_match_forward
from .utils import isLine, span2low, span2pos, span2tag, generate_wildcard, str2span, low2str

class Docs:
    """
    :class A wrapper for spacy.Doc
        :method
    """
    block_num = 1000000
    
    @staticmethod
    def getMatchesDoc(matches, doc):
        texts = []
        for _, start, end in matches:
            texts.append(doc[start:end])
        return texts
    
    @staticmethod
    def partition(file, size = block_num):
        '''
        :return  yield the input file blocks 1000000
        '''
        with open(file, 'r') as f:
            while True:
                data = f.read(size)
                if not data:
                    break
                yield data
    # ----------------------------------------------------
    def __init__(self, filename, load=False):
        self.dir = os.path.dirname(__file__)
        self._file = filename
        self._filebase = os.path.basename(filename)
        self._docs = []
        self._readPtr = 0
        
    def __repr__(self):
        strs=f"<Docs> {self._filebase} => "
        strs = strs + f"have {self._readPtr} docs({Docs.block_num} bytes)"
        return strs
        
    def __getitem__(self, index):
        return self._docs[index]
    
    def __len__(self):
        return self._readPtr
    
    def load(self, name):
        with open(name, 'rb') as f:
            self._docs = pickle.load(f)
            self._readPtr = len(self._docs)
    
    def save(self, name):
        with open(name, 'wb') as f:
            pickle.dump(self._docs, f)
    
    def initialize(self, preload=None):
        print(gstr("Start to load docs"))
        for i, data in tqdm(enumerate(Docs.partition(self._file))):
            if preload is not None and i >= preload:
                break
            doc = NLP(data)
            self._docs.append(doc)
            self._readPtr += 1
    
    def iter(self, shuffle=False):
        index = np.arange(len(self._docs))
        if shuffle:
            np.random.shuffle(index)
        for i in index:
            yield self._docs[i]
    
    def match(self, patterns):
        matcher = Matcher(NLP.vocab)
        matcher.add("_", patterns)
        match_span = []
        for doc in self._docs:
            match = matcher(doc)
            match_span.extend(Docs.getMatchesDoc(match, doc))    
        return match_span
# -------------------------------------------
class Pattern:
    """
    Design for binary relationship
    """
    __Pattern_hash = {}
    __P_id = 0
    
    def __new__(cls, left_phrase, right_phrase):
        """
        Store patterns
            :param: left_phrase tuple(span, span)
            :param: right_phrase tuple(span, span)
        """
        label = (left_phrase[0].text, left_phrase[1].text, right_phrase[0].text, right_phrase[1].text)
        already = cls.__Pattern_hash.get(label, None)
        if already is None:
            cls.__P_id += 1
            self = object.__new__(cls)
            cls.__Pattern_hash[label] = self
            return self
        else:
            already.appear += 1
            return already
    
    @staticmethod
    def patterns():
        return list(Pattern.__Pattern_hash.values())
         
    @staticmethod
    def pattern_num():
        return Pattern.__P_id
    
         
    def __init__(self, left_phrase, right_phrase):
        if not hasattr(self, "appear"):
            self._left = [span2low(left_phrase[0]), span2low(left_phrase[1])]
            self._right = [span2low(right_phrase[0]), span2low(right_phrase[1])]
            self.max_cards = MAX_RELATION - len(self._left[1]) - len(self._right[0])
            assert self.max_cards >= 0
            self.appear = 1
    
    def __repr__(self): 
        return f"<P> {low2str(self._left[0])} #E {low2str(self._left[1])}" \
                " ... " \
               f"{low2str(self._right[0])} #E {low2str(self._right[1])}"
    
    def attribute_pattern(self, one_tuple, left=True):
        """
        :method: phrase, generate matcher rules
            :param: tuple
            :param: left, if true, then use the left attribute to search

            :return: patterns [{...},{...},...]
        """
        if left:
            search = one_tuple[0]
            search = span2low(search)
            # form = one_tuple[1]
            # form = span2pos(form)
            patterns = []
            for i in range(1, MAX_ENTITY+1):
                form = [{}]*i
                patterns.extend(self._phrase(search, form))
        else:
            search = one_tuple[1]
            search = span2low(search)
            patterns = []
            for i in range(1, MAX_ENTITY+1):
                form = [{}]*i
                patterns.extend(self._phrase(form, search))
        return patterns
        
    
    def getTuple(self, span):
        if not pattern_match_forward(0, span, self._left[0]):
            return None
        left_start = len(self._left[0])
        left_end = left_start+1
        while not pattern_match_forward(left_end, span, self._left[1]):
            left_end += 1
        left_entity = span[left_start:left_end]
        end = len(span)
        if not pattern_match_backward(end, span, self._right[1]):
            return None
        right_end = end - len(self._right[1])
        right_start = right_end - 1
        while not pattern_match_backward(right_start, span, self._right[0]):
            right_start -= 1
        right_entity = span[right_start:right_end]
        return Tuple(left_entity, right_entity)
    
    def _phrase(self, left_tuple, right_tuple):
        phrase1 = self._left[0] + left_tuple + self._left[1]
        phrase2 = self._right[0] + right_tuple + self._right[1]
        P_candi = generate_wildcard(phrase1, phrase2, cards=self.max_cards, minimal=0)
        return P_candi


class Tuple:
    """
    desgin for binary relationship
    """
    __Tuple_hash = {}
    __T_id = 0
    def __new__(cls, tuple_left,tuple_right, seed=False):
        """
        Store tuples
            :param: tuple_left str or Span
            :param: tuple_right str or Span
        """
        label = (str(tuple_left), str(tuple_right))
        already = Tuple.__Tuple_hash.get(label, None)
        if already is None:
            self = object.__new__(cls)
            Tuple.__Tuple_hash[label] = self
            Tuple.__T_id += 1
            return self
        else:
            return already
    @staticmethod
    def tuples():
        return list(Tuple.__Tuple_hash.values())
    
    @staticmethod
    def tuple_num():
        return Tuple.__T_id
    
    @staticmethod
    def remainTopK(topk):
        if len(Tuple.__Tuple_hash) <= topk:
            pass
        else:
            arg_sort = sorted(Tuple.__Tuple_hash.items(), key= lambda x : x[1].appear)
            Tuple.__T_id = topk
            for i in range(len(Tuple.__Tuple_hash) - topk):
                if arg_sort[i][1].is_seed():
                    continue
                arg = arg_sort[i][0]
                Tuple.__Tuple_hash.pop(arg)
        return list(Tuple.__Tuple_hash.values())
    
    def __init__(self, tuple_left, tuple_right, seed=False):
        if not hasattr(self, 'appear'):
            tuple_left = tuple_left if isinstance(tuple_left, Span) else str2span(tuple_left)
            tuple_right = tuple_right if isinstance(tuple_right, Span) else str2span(tuple_right)
            self._tuple = (tuple_left, tuple_right)
            self.relationship = {}
            self.appear = 1
            self.__seed = seed
    
    def is_seed(self): return self.__seed
        
    def relate(self, pat : Pattern):
        already = self.relationship.get(pat, None)
        self.appear += 1 
        if already is None:
            self.relationship[pat] = 1
        else:
            self.relationship[pat] += 1
        
    def __getitem__(self, index):
        return self._tuple[index]
    
    def __repr__(self): return "<T> " + str(self._tuple)
