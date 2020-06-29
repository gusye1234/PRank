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

import matplotlib.pyplot as plt
import numpy as np
from rich.progress import track
from rich import print
import os
from os.path import join

# -------------------------------------------
# preload language model(english)
NLP = spacy.load('en_core_web_sm')
infixes = tuple([r"'s\b", r"(?<!\d)\.(?!\d)"]) +  NLP.Defaults.prefixes
infix_re = spacy.util.compile_infix_regex(infixes)
NLP.tokenizer = Tokenizer(NLP.vocab, infix_finditer=infix_re.finditer)

DATAPATH = 'data'
np.set_printoptions(precision=3)

def ystr(param): return f"[bold yellow]{param}[/bold yellow]"
def gstr(param): return f"[bold green]{param}[/bold green]"
def bstr(param): return f"[bold blue]{param}[/bold blue]"
def rstr(param): return f"[bold red]{param}[/bold red]"