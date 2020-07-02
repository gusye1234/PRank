"""
    helper functions
"""
from .world import *

def generate_wildcard(phrase1, phrase2, cards=5, minimal=0):
    """
    return patterns with wildcard between. (phrase1 ... phrase2)
    """
    assert isinstance(phrase1, list) and isinstance(phrase2, list)
    pats = []
    for num_card in range(minimal, cards):
        pats.append(phrase1 + [{}]*num_card + phrase2)
    return pats
# -------------------------------------------
def isLine(line): return not any([(token.is_punct or token.is_space)  for token in line])
# -------------------------------------------
def span2low(span): return [{'LOWER' : token.lower_} for token in span]
def span2pos(span): return [{'POS' : token.pos_} for token in span]
def span2tag(span): return [{'TAG' : token.tag_} for token in span]
def span2text(span): return [{'TEXT' : token.text} for token in span]
def str2span(string): return NLP(string)[:]
def low2str(phrase): return ' '.join([token['LOWER'] for token in phrase])
# -------------------------------------------
def pattern_match_forward(start, span, phrase): 
    for i in range(len(phrase)):
        if span[i+start].lower_ != phrase[i]['LOWER']:
            return False
    return True
def pattern_match_backward(end, span, phrase):
    for i in range(len(phrase)):
        if span[end - i - 1].lower_ != phrase[len(phrase) - i - 1]['LOWER']:
            return False
    return True
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
def generate_toy(filename, lines=1000, maxint=10):
    import numpy as np
    patterns = {
        0 : "plus one is",
        1 : "multiply two is",
        2 : "square is",
        3 : "minus one is",
        4 : "divide two is"
    }
    function = {
        0 : lambda x: x+1,
        1 : lambda x: x*2,
        2 : lambda x: x**2,
        3 : lambda x: x - 1,
        4 : lambda x: x//2
    }
    MAXINT = maxint
    line_num = np.random.randint(1, MAXINT+1, size=lines)
    line_relation = np.random.randint(len(patterns), size=lines)
    line_cont = [
        f"{num} {patterns[choice]} {function[choice](num)} .\n" for num, choice in zip(line_num, line_relation)
    ]
    with open(filename, 'w') as f:
        f.writelines(line_cont)

# -------------------------------------------
def show_library():
    """
    show logo in __main__.py
    """
    from rich import print
    logo="""
.______   .______          ___      .__   __.  __  ___ 
|   _  \  |   _  \        /   \     |  \ |  | |  |/  / 
|  |_)  | |  |_)  |      /  ^  \    |   \|  | |  '  /  
|   ___/  |      /      /  /_\  \   |  . `  | |    <   
|  |      |  |\  \----./  _____  \  |  |\   | |  .  \  
| _|      | _| `._____/__/     \__\ |__| \__| |__|\__\ 
A library for binary-relation tuple extraction
    """
    print("[bold green]"+logo+"[/bold green]")

    inform="""
    Author: Jianbai Ye (叶坚白)
    Mail  : jianbaiye At outlook DOT com"""
    print("[green]"+inform+"[/green]")

if __name__ == "__main__":
    generate_toy("toy.txt", maxint=50)