"""
    Different ways to rank scored items
"""
from .world import *
from .inference import BasicMethod


def precision_rank(results, 
                   inferor : BasicMethod):
    """
    :param: results -> dict, refer to tor.inference
    """
    t_pre = results['tuple precision']
    p_pre = results['pattern precision']
    arg_t = np.argsort(t_pre)
    arg_p = np.argsort(p_pre)
    sort_t = [inferor.id2T[i] for i in arg_t]
    sort_p = [inferor.id2P[i] for i in arg_p]
    return sort_t, sort_p
    
def recall_rank(results, 
                inferor : BasicMethod):
    t_rec = results['tuple recall']
    p_rec = results['pattern recall']
    arg_t = np.argsort(t_rec)
    arg_p = np.argsort(p_rec)
    sort_t = [inferor.id2T[i] for i in arg_t]
    sort_p = [inferor.id2P[i] for i in arg_p]
    return sort_t, sort_p

def f1_score_rank(results, 
                inferor : BasicMethod):
    """
    :return: sorted tuples, patterns
    """
    t_rec = results['tuple recall']
    p_rec = results['pattern recall']
    t_pre = results['tuple precision']
    p_pre = results['pattern precision']
    f1_t = 2*(t_rec*t_pre)/(t_rec + t_pre)
    f1_p = 2*(p_rec*p_pre)/(p_rec + p_pre)
    arg_t = np.argsort(f1_t)
    arg_p = np.argsort(f1_p)
    sort_t = [inferor.id2T[i] for i in arg_t]
    sort_p = [inferor.id2P[i] for i in arg_p]
    return sort_t, sort_p
    