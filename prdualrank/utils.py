"""
    helper functions
"""
import spacy
from spacy.tokens.doc import Doc
from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher
from spacy.tokenizer import Tokenizer
import re

from whoosh.qparser import QueryParser
import whoosh.index as index
from whoosh.index import open_dir
from whoosh.query import Every

from collections import defaultdict

import itertools
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# -------------------------------------------
# preload language model(english)
NLP = spacy.load('en_core_web_sm')
infixes = tuple([r"'s\b", r"(?<!\d)\.(?!\d)"]) +  NLP.Defaults.prefixes
infix_re = spacy.util.compile_infix_regex(infixes)
NLP.tokenizer = Tokenizer(NLP.vocab, infix_finditer=infix_re.finditer)
MATCHER = Matcher(NLP.vocab)


# -------------------------------------------
# def extractor(document, *pattern):
#     '''
#     A phrase extractor based on spacy
#         :param document
#         :param list pattern: extraction pattern
#     :return phrase extraction from 
#     '''
#     phrases = []
#     MATCHER.add("pattern extraction", None, *pattern)
#     doc = document if isinstance(document, Doc) else NLP(document)
#     matches = matcher(doc)
#     for match_id, start, end in matches:
#         # string_id = NLP.vocab.strings[match_id]  # Get string representation
#         span = doc[start:end]  # The matched span
#         phrases.append(span.text)
#     MATCHER.remove('pattern extraction')
#     return phrases

# -------------------------------------------
def partition(file, size = 1000000):
    '''
    :return  yield the input file blocks
    '''
    while True:
        data = file.read(size)
        if not data:
            break
        yield data
        
def show_library():
    from rich import print
    logo="""
,--------.              
'--.  .--',---. ,--.--. 
   |  |  | .-. ||  .--' 
   |  |  ' '-' '|  |    
   `--'   `---' `--'   A library for tuple extraction"""
    print("[bold blue]"+logo+"[/bold blue]")

    inform="""
    Author: Jianbai Ye (叶坚白)
    Mail  : jianbaiye At outlook DOT com"""
    print("[green]"+inform+"[/green]")
