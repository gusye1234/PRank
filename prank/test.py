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
        tuples[0] : {patterns[0]:39, patterns[1] : 1},
        tuples[1] : {patterns[1] : 40},
        tuples[2] : {patterns[1] : 20, patterns[2] : 20},
        tuples[3] : {patterns[2] : 40},
        tuples[4] : {patterns[2] : 40},
        tuples[5] : {patterns[2] : 40},
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
    t3 = utils.str2span("machine learning")
    t4 = utils.str2span("AI")
    p3 = (utils.str2span("The"), utils.str2span("algorithms"))
    p4 = (utils.str2span("of"), utils.str2span("area"))
    assert id(tuple1) == id(object.Tuple(t3, t4))
    assert id(pattern1) == id(object.Pattern(p3, p4))
    
def test_search():
    Tuple = object.Tuple
    Pattern = object.Pattern
    mydoc = object.Docs(os.path.join(
        DATAPATH, 'toy.txt'
    ))
    print(ystr("please wait to load nlp model"))
    mydoc.initialize()    
    searcher = search.PRDualRankSearch(mydoc)
    seeds = set([
        Tuple("1", "2", seed=True), Tuple('2', '4', seed=True), 
        Tuple("3", '6', seed=True), Tuple('4', '8', seed=True)
    ])
    patterns = set([])
    tuples = set([])
    tuples.update(seeds)
    for i in range(2):
        # patterns.update(searcher.fromTuple2Pattern(tuples))
        searcher.fromTuple2Pattern(Tuple.tuples())
        # tuples.update(searcher.fromPattern2Tuple(patterns, tuples))
        searcher.fromPattern2Tuple(Pattern.patterns(), Tuple.tuples())
        
    print(ystr(f"Found {Pattern.pattern_num()} patterns"))
    print(ystr(f"Found {Tuple.tuple_num()} tuples"))
    print(Pattern.patterns())
    print(Tuple.tuples())
    tuples = Tuple.remainTopK(10)
    relation = {
        tup : tup.relationship for tup in tuples
    }
    inferor = inference.PRDualRank()
    results = inferor.infer(
        Tuple.tuples(),
        Pattern.patterns(),
        relation,
        seed_tuples=list(seeds),
        max_iter=5
    )
    top_t, top_p = rank.f1_score_rank(results, inferor)
    print(gstr("Top-5 tuples:"), top_t[-8:])
    print(gstr("Top-2 patterns:"), top_p[-2:])
    
if __name__ == "__main__":
    # test_docs()
    # test_infer()
    # test_objects()
    test_search()