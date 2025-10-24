import random
import networkx as nx
from collections import Counter
from typing import Dict, Iterable, List, Set, Tuple
from ..graph_utils import as_edge, all_nodes_from_edges

SamplerFn = callable

_SAMPLERS: Dict[str, SamplerFn] = {}

def register_sampler(name: str):
    def deco(fn: SamplerFn):
        _SAMPLERS[name] = fn
        return fn
    return deco

def get_sampler(name: str) -> SamplerFn:
    if name not in _SAMPLERS:
        raise KeyError(f"Unknown Samplers: {name}. Chosen: {list(_SAMPLERS)}")
    return _SAMPLERS[name]

@register_sampler("random")
def sample_random_visible(
    visible_pos_edges: Iterable[Tuple[int, int]],
    num_samples: int,
    seed: int,
    nodes: Iterable[int] | None = None,
) -> List[Tuple[int, int]]:
    """
    Perform uniform negative sampling on the "visible graph" patch:
    - visible_pos_edges: All visible positive edges (undirected) at this stage
    - nodes: The complete set of nodes (can be empty; if empty, it is inferred from visible_pos_edges)
    - num_samples: The number of negative samples required
    """
    pos_set: Set[Tuple[int, int]] = set(as_edge(u, v) for (u, v) in visible_pos_edges if u != v)
    if nodes is None:
        nodes = all_nodes_from_edges(pos_set)
    node_list = list(set(int(n) for n in nodes))
    n = len(node_list)
    if n < 2:
        raise ValueError("Not enough nodes for negative sampling.")
    max_non_edges = n * (n - 1) // 2 - len(pos_set)
    if num_samples > max_non_edges:
        raise ValueError(f"Insufficient image capacity: Maximum {max_non_edges}, request {num_samples}。")

    rnd = random.Random(seed)
    negs: Set[Tuple[int, int]] = set()
    idx = {i: node_list[i] for i in range(n)}
    tries = 0
    limit = max(10000, num_samples * 50)
    while len(negs) < num_samples and tries < limit:
        i = rnd.randrange(n); j = rnd.randrange(n)
        if i == j:
            tries += 1; continue
        u, v = as_edge(idx[i], idx[j])
        if (u, v) in pos_set or (u, v) in negs:
            tries += 1; continue
        negs.add((u, v))
    if len(negs) < num_samples:
        raise RuntimeError("Failure to collect enough negative samples (random rejection sampling is limited).")
    return list(negs)

@register_sampler("degree_weighted")
def sample_degree_weighted(
    visible_pos_edges,
    num_samples,
    seed,
    nodes=None,
):
    """
    度加权采样：在可见图的补图上，按度乘积加权抽样。
    （越大度节点越容易被采到，模拟hard negative）
    """

    rnd = random.Random(seed)
    pos_set = set(as_edge(u, v) for u, v in visible_pos_edges if u != v)
    if nodes is None:
        nodes = all_nodes_from_edges(pos_set)
    nlist = list(nodes)
    n = len(nlist)

    # 统计度
    deg = Counter()
    for u, v in visible_pos_edges:
        deg[u] += 1
        deg[v] += 1

    # 计算采样权重（按度乘积）
    weights = []
    pairs = []
    for i in range(n):
        for j in range(i + 1, n):
            u, v = nlist[i], nlist[j]
            if (u, v) in pos_set:
                continue
            pairs.append((u, v))
            weights.append((deg[u] + 1) * (deg[v] + 1))

    # 归一化采样
    total = sum(weights)
    probs = [w / total for w in weights]
    neg_edges = rnd.choices(pairs, weights=probs, k=num_samples)
    return neg_edges
