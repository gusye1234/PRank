import spacy
from spacy.tokens.doc import Doc
from .world import *
from tqdm import tqdm
import numpy as np
import pickle
from .utils import isLine, span2low, span2pos, span2tag, generate_wildcard, str2span

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
        strs=f"<Docs> {self._filebase} "
        strs = strs + f"have {self._readPtr} docs, each with {Docs.block_num} bytes"
        return strs
        
    def load(self, name):
        with open(name, 'rb') as f:
            self._docs = pickle.load(f)
            self._readPtr = len(self._docs)
    
    def save(self, name):
        with open(name, 'wb') as f:
            pickle.dump(self._docs, f)
    
    def initialize(self, preload=None):
        print("[bold yellow]Start to load docs[/bold yellow]")
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
        matcher.add("_", None, *patterns)
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
    Pattern_hash = {}
    P_id = 0
    def __new__(cls, left_phrase, right_phrase):
        """
        Store patterns
            :param: left_phrase tuple(span, span)
            :param: right_phrase tuple(span, span)
        """
        already = cls.Pattern_hash.get((left_phrase, right_phrase), None)
        if already is None:
            cls.P_id += 1
            self = object.__new__(cls)
            cls.__init__(self, left_phrase, right_phrase)
            cls.Pattern_hash[(left_phrase, right_phrase)] = self
            return self
        else:
            return already
         
    def __init__(self, left_phrase, right_phrase):
        self.left = [span2low(left_phrase[0]), span2low(left_phrase[1])]
        self.right = [span2low(right_phrase[0]), span2low(right_phrase[1])]
        self.max_cards = 10 - len(self.left[1]) - len(self.right[0])
        assert self.max_cards > 0
    
    def __repr__(self): return f"{self.left[0]}~#E~{self.left[1]}...{self.right[0]}~#E~{self.right[1]}"
    
    def attribute_search(self, one_tuple, left=True):
        """
        :method: phrase, generate matcher rules
            :param: tuple
            :param: left, if true, then use the left attribute to search
        """
        if left:
            search = one_tuple[0]
            search = span2low(search)
            form = one_tuple[1]
            form = span2pos(form)
            return self._phrase(search, form)
        else:
            search = one_tuple[1]
            search = span2low(search)
            form = one_tuple[0]
            form = span2pos(form)
            return self._phrase(form, search)
            
    
    def _phrase(self, left_tuple, right_tuple):
        phrase1 = self.left[0] + left_tuple + self.left[1]
        phrase2 = self.right[0] + right_tuple + self.right[1]
        P_candi = generate_wildcard(phrase1, phrase2, cards=self.max_cards, minimal=1)
        return P_candi


class Tuple:
    Tuple_hash = {}
    T_id = 0
    def __new__(cls, tuple_left,tuple_right):
        """
        Store tuples
            :param: tuple_left str or Span
            :param: tuple_right str or Span
        """
        tuple_left = tuple_left if isinstance(tuple_left, Span) else str2span(tuple_left)
        tuple_right = tuple_left if isinstance(tuple_right, Span) else str2span(tuple_right)
        already = Tuple.Tuple_hash.get((tuple_left,tuple_right), None)
        if already is None:
            self = object.__new__(cls)
            cls.__init__(self, tuple_left, tuple_right)
            Tuple.Tuple_hash[(tuple_left, tuple_right)] = self
            Tuple.T_id += 1
            return self
        else:
            return already
        
    
    def __init__(self, tuple_left, tuple_right):
        self._tuple = (tuple_left, tuple_right)
        self.relationship = {}
        
    def relate(self, pat : Pattern):
        already = self.relationship.get(pat, None)
        if already is None:
            self.relationship[pat] = 1
        else:
            self.relationship[pat] += 1
        
    def __getitem__(self, index):
        return self._tuple[index]
    
    def __repr__(self): return str(self._tuple)
