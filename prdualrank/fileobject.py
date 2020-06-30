import spacy
from spacy.tokens.doc import Doc
from .world import *
from tqdm import tqdm
import numpy as np
import pickle

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