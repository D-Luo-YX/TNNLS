import os
from typing import List, Tuple
from .graph_utils import load_edges_txt, save_edges_txt, all_nodes_from_edges
from .split_methods.strategies import get_tp_splitter
from .negative_sampling.samplers import get_sampler

def run_TP(
    filename: str,
    project_root: str,
    split_strategy: str,   # e.g., "random"
    sampler_name: str,     # e.g., "random_visible"
    test_ratio: float,
    split_seed1: int,
) -> str:
    """
    输入：datasets/raw/{filename}.txt
    输出：datasets/{filename}/TP_{split_seed1}/
      - Train_pos.txt, Test_pos.txt, Test_neg.txt
    说明：Test_neg 在“全图可见”补图上采样，数量=|Test_pos|
    """
    raw_path = os.path.join(project_root, "datasets", "raw", f"{filename}.txt")
    edges = load_edges_txt(raw_path)
    nodes = all_nodes_from_edges(edges)

    # 选择 TP 划分策略
    tp_split = get_tp_splitter(split_strategy)
    train_pos, test_pos = tp_split(edges, test_ratio, split_seed1)

    # 选择 抽样器（P阶段可见=全图）
    sampler = get_sampler(sampler_name)
    test_neg = sampler(visible_pos_edges=edges, num_samples=len(test_pos),
                       seed=split_seed1 + 100, nodes=nodes)

    out_dir = os.path.join(project_root, "datasets", filename, f"TP_{split_seed1}")
    save_edges_txt(os.path.join(out_dir, "Train_pos.txt"), train_pos)
    save_edges_txt(os.path.join(out_dir, "Test_pos.txt"), test_pos)
    save_edges_txt(os.path.join(out_dir, "Test_neg.txt"), test_neg)
    return out_dir
