from date_process.loaders import *
# src/test.py
from graph_ops.TP_main import run_TP
from graph_ops.TV_main import run_TV

if __name__ == "__main__":
    project_root = "."
    filename = "USAir"     # 对应 datasets/raw/USAir.txt

    # === 选择策略（名称即注册名） ===
    tp_split_strategy = "random"
    tv_split_strategy = "random"
    sampler_name = "random"

    # === 超参数（可随实验改动） ===
    test_ratio  = 0.10
    val_ratio   = 0.10
    split_seed1 = 42
    split_seed2 = 42

    tp_out = run_TP(
        filename=filename,
        project_root=project_root,
        split_strategy=tp_split_strategy,
        sampler_name=sampler_name,
        test_ratio=test_ratio,
        split_seed1=split_seed1,
    )
    print("[TP] Output:", tp_out)

    tv_out = run_TV(
        filename=filename,
        project_root=project_root,
        split_seed1=split_seed1,
        split_strategy=tv_split_strategy,
        sampler_name=sampler_name,
        val_ratio=val_ratio,
        split_seed2=split_seed2,
    )
    print("[TV] Output:", tv_out)

    print("All done.")