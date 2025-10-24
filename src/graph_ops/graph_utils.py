import os
from typing import Iterable, List, Tuple, Set

def as_edge(u: int, v: int) -> Tuple[int, int]:
    return (u, v) if u < v else (v, u)

def load_edges_txt(path: str) -> List[Tuple[int, int]]:
    edges = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            u, v = map(int, line.strip().split())
            if u == v:  # 禁止自环
                continue
            edges.append(as_edge(u, v))
    # 去重
    return list(set(edges))

def save_edges_txt(path: str, edges: Iterable[Tuple[int, int]]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for u, v in edges:
            f.write(f"{u} {v}\n")

def all_nodes_from_edges(edges: Iterable[Tuple[int, int]]) -> List[int]:
    s: Set[int] = set()
    for u, v in edges:
        s.add(u); s.add(v)
    return sorted(s)