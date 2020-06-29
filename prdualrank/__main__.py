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
    phrase1 = utils.str2phrase("is the")
    phrase2 = utils.str2phrase("of")
    patterns= utils.generate_wildcard(phrase1, phrase2, cards=5)
    print(patterns)
    mydoc = fileobject.Docs(os.path.join(
        DATAPATH, 'clean.txt'
    ))
    mydoc.initialize(preload=20)
    mydoc.save()
    mydoc.load()
    print(mydoc.match(patterns))
    print(mydoc)
    for doc in mydoc.iter():
        print(doc[:10], '...')
    
    
if __name__ == "__main__":
    test_docs()