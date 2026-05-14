# -*- coding: utf-8 -*-
import math
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif']='SimHei'

def min_entropy_to_p(h_min):
    """反解最小熵对应的最大概率"""
    return 2 ** (-h_min)

def xor_min_entropy(p, n):
    """计算 n 个 Bern(p) 异或后的最小熵"""
    # 计算 XOR 后的概率 q
    q = (1 - (1 - 2 * p) ** n) / 2
    p_xor = max(q, 1 - q)
    return -math.log2(p_xor)

def plot_min_entropy_growth(hmin, max_n=32):
    p = min_entropy_to_p(hmin)
    x_vals = list(range(1, max_n + 1))
    y_vals = [xor_min_entropy(p, n) for n in x_vals]

    # 打印n和对应的熵值
    print("\nn值与对应的最小熵结果：")
    print("-" * 30)
    print("n\t最小熵(bits)")
    print("-" * 30)
    for n, h in zip(x_vals, y_vals):
        print(f"{n}\t{h:.6f}")
    print("-" * 30)

    plt.figure(figsize=(8, 5))
    plt.plot(x_vals, y_vals, marker='o')
    plt.axhline(y=1.0, color='red', linestyle='--', label='Full Entropy (1 bit)')
    plt.title(f"最小熵增长曲线 (原始概率 p = {p:.6f})")
    plt.xlabel("异或个数 n")
    plt.ylabel("XOR 后最小熵 (bits)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # fro2sro3 h=0.221294

    # fro2sro4 h=
    # fro3sro4 h=

    # fro2sro5 h=
    # fro3sro5 h=
    # fro4sro5 h=

    # fro2sro6 h=
    # fro3sro6 h=
    # fro4sro6 h=
    # fro5sro6 h=

    # fro2sro7 h=
    # fro3sro7 h=
    # fro4sro7 h=
    # fro5sro7 h=
    # fro6sro7 h=

    # fro2sro8 h=
    # fro3sro8 h=
    # fro4sro8 h=
    # fro5sro8 h=
    # fro6sro8 h=
    # fro7sro8 h=

    # fro2sro9 h=0.257902
    # fro3sro9 h=0.155214
    # fro4sro9 h=
    # fro5sro9 h=
    # fro6sro9 h=
    # fro7sro9 h=0.234520
    # fro8sro9 h=0.234496
    
    plot_min_entropy_growth(0.257902)
