import os
from typing import List, Tuple, Set
from .graph_utils import load_edges_txt, save_edges_txt, all_nodes_from_edges
from .split_methods.strategies import get_tv_splitter
from .negative_sampling.samplers import get_sampler

def run_TV(
    filename: str,
    project_root: str,
    split_seed1: int,      # 读取 TP 层产物
    split_strategy: str,   # e.g., "random"
    sampler_name: str,     # e.g., "random_visible"
    val_ratio: float,
    split_seed2: int,
) -> str:
    """
    输入：datasets/{filename}/TP_{split_seed1}/Train_pos.txt
    输出：datasets/{filename}/TP_{split_seed1}/TV_{split_seed2}/
      - Train_pos.txt (T_pos), Train_neg.txt  （在 T 可见）
      - Val_pos.txt   (V_pos), Val_neg.txt    （在 T+V 可见）
    """
    tp_dir = os.path.join(project_root, "datasets", filename, f"TP_{sampler_name}_{split_seed1}")
    base_train_pos = load_edges_txt(os.path.join(tp_dir, "Train_pos.txt"))

    # TV 划分
    tv_split = get_tv_splitter(split_strategy)
    T_pos, V_pos = tv_split(base_train_pos, val_ratio, split_seed2)

    # 可见集合
    T_visible = T_pos
    TV_visible = T_pos + V_pos

    # 节点全集（建议使用原始全图防止节点缺失）
    raw_edges = load_edges_txt(os.path.join(project_root, "datasets", "raw", f"{filename}.txt"))
    nodes = all_nodes_from_edges(raw_edges)

    # 负采样
    sampler = get_sampler(sampler_name)
    Train_neg = sampler(T_visible, num_samples=len(T_pos), seed=split_seed2 + 11, nodes=nodes)
    Val_neg   = sampler(TV_visible, num_samples=len(V_pos), seed=split_seed2 + 22, nodes=nodes)

    out_dir = os.path.join(tp_dir, f"TV_{sampler_name}_{split_seed2}")
    save_edges_txt(os.path.join(out_dir, "Train_pos.txt"), T_pos)
    save_edges_txt(os.path.join(out_dir, "Train_neg.txt"), Train_neg)
    save_edges_txt(os.path.join(out_dir, "Val_pos.txt"), V_pos)
    save_edges_txt(os.path.join(out_dir, "Val_neg.txt"), Val_neg)
    return out_dir