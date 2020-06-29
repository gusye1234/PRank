"""
    helper functions
"""
from .world import *


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
#     matches = MATCHER(doc)
#     for match_id, start, end in matches:
#         # string_id = NLP.vocab.strings[match_id]  # Get string representation
#         span = doc[start:end]  # The matched span
#         phrases.append(span.text)
#     MATCHER.remove('pattern extraction')
#     return phrases
# -------------------------------------------
def generate_wildcard(phrase1, phrase2, cards=5):
    """
    return patterns with wildcard between. (phrase1 ... phrase2)
    """
    assert isinstance(phrase1, list) and isinstance(phrase2, list)
    pats = []
    for num_card in range(cards):
        pats.append(phrase1 + [{}]*num_card + phrase2)
    return pats

# -------------------------------------------
def str2phrase(string : str, tag="LOWER"):
    strs = string.split()
    phrase = []
    for token in strs:
        phrase.append({tag:token})
    return phrase
# -------------------------------------------
def clean_data(filename, new_name):
    """
    exclude line started with "< | !"
    """
    from rich.progress import track
    into = open(new_name, 'w')
    with open(filename, 'r') as f:
        for line in track(f.readlines()):
            if line.startswith('<') or line.startswith('!'):
                continue
            if line.strip() and len(line.split()) >= 10:
                into.write(line)
    into.close()

# -------------------------------------------
def show_library():
    """
    show logo in __main__.py
    """
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
