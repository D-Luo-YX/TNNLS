#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def print_graph_info(path: str):
    nodes = set()
    edges_undirected = set()   # 使用 (min(u,v), max(u,v)) 表示无向边
    self_loops = 0
    duplicate_edges = 0
    bad_lines = 0
    total_lines = 0

    try:
        with open(path, "r", encoding="utf-8") as f:
            for lineno, line in enumerate(f, start=1):
                total_lines += 1
                s = line.strip()
                if not s or s.startswith("#"):  # 跳过空行和注释
                    continue

                parts = s.split()
                if len(parts) != 2:
                    bad_lines += 1
                    continue

                try:
                    u, v = int(parts[0]), int(parts[1])
                except ValueError:
                    bad_lines += 1
                    continue

                # 记录节点
                nodes.add(u)
                nodes.add(v)

                # 自环单独统计，不计入无向边集合（如需计入，可修改）
                if u == v:
                    self_loops += 1
                    continue

                # 统一无向边表示
                e = (u, v) if u < v else (v, u)
                if e in edges_undirected:
                    duplicate_edges += 1
                else:
                    edges_undirected.add(e)

    except Exception as e:
        print(f"[ERROR] 无法读取文件：{path}")
        print(f"具体错误：{e}")
        return

    print("========== Graph Info (Undirected) ==========")
    print(f"File Path                    : {path}")
    print(f"Total Lines Read             : {total_lines}")
    print(f"Valid Nodes                  : {len(nodes)}")
    print(f"Unique Undirected Edges      : {len(edges_undirected)}  (不含自环)")
    print(f"Self-loops (u==v)            : {self_loops}")
    print(f"Duplicate Edge Lines         : {duplicate_edges}")
    print(f"Bad/Skipped Lines            : {bad_lines}")
    print("---------------------------------------------")
    print("说明：无向图，(u,v) 与 (v,u) 视为同一条边；自环未计入边数。")
    print("=============================================")

if __name__ == "__main__":
    # ======== 直接修改下面这一行即可 ========
    # file_path = ("raw/USAir.txt")
    # ==========================================
    # print_graph_info(file_path)

    file_path = ("USAir/TP_42/Test_pos.txt")
    print_graph_info(file_path)

    file_path = ("USAir/TP_42/TV_42/Train_pos.txt")
    print_graph_info(file_path)