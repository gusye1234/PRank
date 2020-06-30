"""
    To run test
"""
from .world import *
from . import object
from . import rank
from . import utils
from . import search
from . import inference



# utils.show_library()
def test_docs():
    phrase1 = utils.str2phrase("natural language processing")
    phrase2 = utils.str2phrase("machine learning")
    patterns= utils.generate_wildcard(phrase1, phrase2, cards=10)
    print(patterns)
    mydoc = object.Docs(os.path.join(
        DATAPATH, 'arxiv_titles_and_abstracts.txt'
    ))
    mydoc.initialize(preload=5)
    # mydoc.save('toy.pth')
    # mydoc.load('test.pth')
    print("load done")
    print(mydoc.match(patterns))
    print(mydoc)
    for i, doc in enumerate(mydoc.iter()):
        print(f"[bold yellow]Doc {i}:[/bold yellow]",doc[:3], '...')

def test_infer():
    tuples = [(1,2), (3,6), (2, 4), (5,25), (6,36), (7, 49)]
    patterns=["plus one", "* 2", "square"]
    relation = {
        tuples[0] : [(patterns[0], 39), (patterns[1], 1)],
        tuples[1] : [(patterns[1], 40)],
        tuples[2] : [(patterns[1], 20), (patterns[2], 20)],
        tuples[3] : [(patterns[2], 40)],
        tuples[4] : [(patterns[2], 40)],
        tuples[5] : [(patterns[2], 40)],
    }
    inferor = inference.PRDualRank()
    results = inferor.infer(tuples, patterns, relation, seed_tuples=[tuples[0]], max_iter=20) 
    print(results)
      
def test_objects():
    t1 = utils.str2span("machine learning")
    t2 = utils.str2span("AI")
    p1 = (utils.str2span("The"), utils.str2span("algorithms"))
    p2 = (utils.str2span("of"), utils.str2span("area"))
    tuple1 = object.Tuple(t1, t2)
    pattern1 = object.Pattern(p1, p2)
    print(tuple1)
    print(pattern1)
    assert id(tuple1) == id(object.Tuple(t1, t2))
    assert id(pattern1) == id(object.Pattern(p1, p2))
    
if __name__ == "__main__":
    # test_docs()
    # test_infer()
    test_objects()