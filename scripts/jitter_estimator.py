# -*- coding: utf-8 -*-
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
import glob
import os

plt.rcParams['font.sans-serif']='SimHei'

add_256_flag = 0

# 固定的窗口大小列表，每个文件对应一个窗口大小（单位：ns）
window_sizes_lutl = [50*5.0, 40*5.0, 80*5.0,
                90*5.0, 125*5.0, 120*5.0, 135*5.0,
                160*5.0]  # RO1, RO2, ...
window_num = 50000  # 使用的窗口数量

# def read_counter_file_u8(filename, window_num):
#     with open(filename, 'rb') as f:
#         data = f.read(window_num)
#         counts = np.frombuffer(data, dtype=np.uint8)
#     return counts.astype(np.float64)

def read_counter_file_u8(filename, window_num):
    with open(filename, 'rb') as f:
        data = f.read(window_num)
        counts = np.frombuffer(data, dtype=np.uint8).astype(np.uint16)
        if add_256_flag == 1:
            counts = counts + 256

    if len(counts) < 2:
        return counts

    mean = np.mean(counts)
    # 使用固定差值阈值判断
    max_deviation=10
    mask = np.abs(counts - mean) <= max_deviation

    removed = counts[~mask]
    filtered = counts[mask]

    if len(removed) > 0:
        unique_removed = sorted(set(removed.tolist()))
        print(f"\n文件 {filename} 剔除 {len(removed)} 个异常点（偏差超过 ±{max_deviation}）：")
        print("剔除数据（唯一值）:", unique_removed)

    return filtered


def estimate_shannon_entropy(counts):
    counter = Counter(counts)
    total = len(counts)
    probs = np.array([v / total for v in counter.values()])
    entropy = -np.sum(probs * np.log2(probs))
    return entropy

def estimate_min_entropy(counts):
    counter = Counter(counts)
    total = len(counts)
    max_p = max(counter.values()) / total
    return -np.log2(max_p)

def analyze_file(filename, window_ns, window_num):
    counts = read_counter_file_u8(filename, window_num)
    C_bar = np.mean(counts)
    var_C = np.var(counts, ddof=1)
    delta_var = var_C * (window_ns / (C_bar**2))**2
    delta_std_ps = np.sqrt(delta_var) * 1000
    ro_freq_mhz = C_bar / window_ns * 1000
    shannon_entropy = estimate_shannon_entropy(counts)
    min_entropy = estimate_min_entropy(counts)

    return {
        "file": filename,
        "mean_count": C_bar,
        "ro_freq_mhz": ro_freq_mhz,
        "jitter_std_ps": delta_std_ps,
        "shannon_entropy": shannon_entropy,
        "min_entropy": min_entropy
    }

def plot_metric(metric_list, titles, ylabel, filename):
    x = np.arange(len(metric_list))
    plt.figure(figsize=(8, 4))
    plt.bar(x, metric_list, tick_label=[f"RO{i+1}" for i in x], color='steelblue')
    plt.ylabel(ylabel)
    plt.title(titles)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

def batch_analyze_ro_files(files, window_sizes, window_num):
    results = []

    if not files:
        print("未找到匹配文件。")
        return

    print(f"{'文件':<12} {'Freq(MHz)':>10} {'Jitter(ps)':>12} {'Shannon':>10} {'MinEntropy':>12} {'MeanCount':>10}")
    print("-" * 80)

    for i, file in enumerate(files):
        # 根据文件顺序从窗口大小列表中获取窗口大小
        window_ns = window_sizes[i] if i < len(window_sizes) else window_sizes[-1]  # 如果窗口大小不足，则使用最后一个
        result = analyze_file(file, window_ns, window_num)
        print(f"{os.path.basename(file):<12} "
              f"{result['ro_freq_mhz']:>10.4f} "
              f"{result['jitter_std_ps']:>12.3f} "
              f"{result['shannon_entropy']:>10.4f} "
              f"{result['min_entropy']:>12.4f}"
              f"{result['mean_count']:>12.4f} ")
        results.append(result)

    # 提取指标
    freqs = [r['ro_freq_mhz'] for r in results]
    jitters = [r['jitter_std_ps'] for r in results]
    shannons = [r['shannon_entropy'] for r in results]
    mins = [r['min_entropy'] for r in results]

    # 绘图
    plot_metric(freqs, "RO 平均频率", "MHz", "freq.png")
    plot_metric(jitters, "RO 抖动标准差", "ps", "jitter.png")
    plot_metric(shannons, "香农熵", "bits", "shannon_entropy.png")
    plot_metric(mins, "最小熵", "bits", "min_entropy.png")

    print("图像已保存为 freq.png, jitter.png, shannon_entropy.png, min_entropy.png")
    return results

def plot_all_metrics(results):
    labels = [os.path.basename(r['file']) for r in results]
    freqs = [r['ro_freq_mhz'] for r in results]
    jitters = [r['jitter_std_ps'] for r in results]
    shannons = [r['shannon_entropy'] for r in results]
    mins = [r['min_entropy'] for r in results]

    fig, axs = plt.subplots(2, 2, figsize=(12, 8))
    axs = axs.flatten()
    metric_data = [freqs, jitters, shannons, mins]
    titles = ["RO 平均频率 (MHz)", "抖动标准差 (ps)", "香农熵 (bits)", "最小熵 (bits)"]

    for i in range(4):
        axs[i].bar(range(len(labels)), metric_data[i], color='steelblue')
        axs[i].set_title(titles[i])
        axs[i].set_xticks(range(len(labels)))
        axs[i].set_xticklabels(labels, rotation=45, ha='right')
        axs[i].grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()
    plt.savefig("summary.png")
    plt.close()
    print("已保存综合图像 summary.png")

if __name__ == "__main__":
    files_lutl = sorted(glob.glob("../data/lutl/RO*.DAT"))
    results = batch_analyze_ro_files(files_lutl, window_sizes_lutl, window_num)
    if results:
        plot_all_metrics(results)