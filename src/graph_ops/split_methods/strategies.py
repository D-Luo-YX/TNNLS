import random
from typing import Dict, List, Tuple

SplitFn = callable

# --- 策略注册表 ---
_TP_SPLITTERS: Dict[str, SplitFn] = {}
_TV_SPLITTERS: Dict[str, SplitFn] = {}

def register_tp_splitter(name: str):
    def deco(fn: SplitFn):
        _TP_SPLITTERS[name] = fn
        return fn
    return deco

def register_tv_splitter(name: str):
    def deco(fn: SplitFn):
        _TV_SPLITTERS[name] = fn
        return fn
    return deco

def get_tp_splitter(name: str) -> SplitFn:
    if name not in _TP_SPLITTERS:
        raise KeyError(f"Unknown TP Split Strategies: {name}. Chosen: {list(_TP_SPLITTERS)}")
    return _TP_SPLITTERS[name]

def get_tv_splitter(name: str) -> SplitFn:
    if name not in _TV_SPLITTERS:
        raise KeyError(f"Unknown TV Split Strategies: {name}. Chosen: {list(_TV_SPLITTERS)}")
    return _TV_SPLITTERS[name]

# ---------- random ----------
@register_tp_splitter("random")
def tp_random_split(edges: List[Tuple[int, int]], test_ratio: float, seed: int):
    """
    Input edges To Random Split: Train_pos / Test_pos
    """
    assert 0.0 < test_ratio < 1.0
    rnd = random.Random(seed)
    arr = edges[:]
    rnd.shuffle(arr)
    m = len(arr)
    m_test = max(1, int(round(m * test_ratio)))
    test_pos = arr[:m_test]
    train_pos = arr[m_test:]
    return train_pos, test_pos

@register_tv_splitter("random")
def tv_random_split(train_pos_edges: List[Tuple[int, int]], val_ratio: float, seed: int):
    """
    Input Train_pos(From T) To Random Split: T_pos / V_pos
    """
    assert 0.0 < val_ratio < 1.0
    rnd = random.Random(seed)
    arr = train_pos_edges[:]
    rnd.shuffle(arr)
    m = len(arr)
    m_val = max(1, int(round(m * val_ratio)))
    V_pos = arr[:m_val]
    T_pos = arr[m_val:]
    return T_pos, V_pos