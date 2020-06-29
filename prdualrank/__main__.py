"""
    To run test
"""
from .world import *
from . import fileobject
from . import rank
from . import utils
from . import search
from . import inference



# utils.show_library()
def test_docs():
    phrase1 = utils.str2phrase("natural language processing")
    phrase2 = utils.str2phrase("machine learning")
    patterns= utils.generate_wildcard(phrase1, phrase2, cards=5)
    print(patterns)
    mydoc = fileobject.Docs(os.path.join(
        DATAPATH, 'arxiv_titles_and_abstracts.txt'
    ))
    mydoc.initialize()
    mydoc.save('test.pth')
    mydoc.load('test.pth')
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
      
    
if __name__ == "__main__":
    test_docs()
    # test_infer()