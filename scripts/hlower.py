import math
from scipy.special import comb
from scipy.optimize import bisect
import matplotlib.pyplot as plt

def calculate_H_lower(f1, f2, sigma1, sigma2):
    """
    计算 H_lower 的函数，基于公式：
    Q = (σ1 * f1)^2 * (f1 / f2) + (σ2 * f1)^2
    H_lower = 1 - (4 / (π^2 * ln(2))) * exp(-4π^2 * Q)
    
    参数:
    f1: float - 快速RO频率 (Hz)
    f2: float - 慢速RO频率 (Hz)
    sigma1: float - 快速RO的抖动标准差
    sigma2: float - 慢速RO的抖动标准差

    返回:
    H_lower: float - 熵下界估计
    """
    pi_sq = math.pi ** 2
    ln2 = math.log(2)

    # 根据你给的新公式计算 Q
    Q = (sigma1 * f1) ** 2 * (f1 / f2) + (sigma2 * f1) ** 2

    # 计算 H_lower
    H_lower = 1 - (4 / (pi_sq * ln2)) * math.exp(-4 * pi_sq * Q)

    return H_lower

def binary_entropy(p):
    """香农熵 H(p)"""
    if p == 0 or p == 1:
        return 0.0
    return -p * math.log2(p) - (1 - p) * math.log2(1 - p)


def find_p_from_entropy(H_target):
    """给定熵H，反解最小的 p，使 H(p) = H_target，取 p ∈ (0, 0.5]"""
    def func(p):
        return binary_entropy(p) - H_target
    return bisect(func, 1e-9, 0.5 - 1e-9)


def xor_output_probability(p, n):
    """n个Bernoulli(p)独立比特异或后，输出为1的概率 q_n"""
    q = 0.0
    for k in range(1, n + 1, 2):  # 奇数项求和
        q += comb(n, k) * (p ** k) * ((1 - p) ** (n - k))
    return q


def xor_entropy_from_Hlower(H_lower, n):
    """已知每个RO的最小熵H_lower，计算n个RO异或后的输出熵"""
    p = find_p_from_entropy(H_lower)
    q = xor_output_probability(p, n)
    return binary_entropy(q)


def plot_entropy_vs_n_from_Hlower(H_lower):
    ns = list(range(1, 33))
    entropies = [xor_entropy_from_Hlower(H_lower, n) for n in ns]
    plt.figure(figsize=(10, 6))
    plt.plot(ns, entropies, marker='o', label=f'H_lower = {H_lower}')
    plt.xlabel('Number of XORed ROs (n)')
    plt.ylabel('Output Bit Entropy (bits)')
    plt.title('Entropy vs n (from H_lower)')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # RO2-RO9的频率和抖动数据
    ro_data = {
        2: {"f": 885.8e6, "sigma": 4.53e-12},
        3: {"f": 1061.1e6, "sigma": 3.73e-12},
        4: {"f": 584.2e6, "sigma": 4.94e-12},  # 请替换为实际数据
        5: {"f": 502.8e6, "sigma": 6.08e-12},  # 请替换为实际数据
        6: {"f": 382.8e6, "sigma": 6.84e-12},  # 请替换为实际数据
        7: {"f": 369.0e6, "sigma": 6.49e-12},  # 请替换为实际数据
        8: {"f": 338.2e6, "sigma": 7.38e-12},  # 请替换为实际数据
        9: {"f": 286.8e6, "sigma": 8.43e-12},  # 请替换为实际数据
    }

    # 打印表头
    print("\n符合条件的RO组合 (entropy >= 0.997):")
    print("-" * 75)
    print(f"{'ROx':<3}{'ROy':<3}{'f1(Hz)':<8}{'f2(Hz)':<8}{'σ1':<10}{'σ2':<10}{'H_lower':<8}{'Entropy':<8}{'n':<3}")
    print("-" * 75)
    print(2 ** (-0.9362))
    print(1 - 2 ** (-0.9362))
    
    # 遍历所有可能的组合
    for x in range(2, 9):  # ROx: 2-8
        for y in range(x + 1, 10):  # ROy: x+1 到 9
            f1 = ro_data[x]["f"]
            f2 = ro_data[y]["f"]
            sigma1 = ro_data[x]["sigma"]
            sigma2 = ro_data[y]["sigma"]

            # 计算H_lower
            H_lower = calculate_H_lower(f1, f2, sigma1, sigma2)

            # 遍历n直到找到满足条件的最小值
            n = 1
            while n <= 32:  # 设置一个上限防止无限循环
                entropy = xor_entropy_from_Hlower(H_lower, n)
                if entropy >= 0.997:
                    # 相应地修改输出格式
                    print(f"RO{x:<2}RO{y:<2}{f1:<8.0f}{f2:<8.0f}{sigma1:<10.2e}{sigma2:<10.2e}"
                          f"{H_lower:<8.4f}{entropy:<8.4f}n={n:<2}")
                    break
                n += 1
                
    print("-" * 80)

    # 可视化趋势
    # plot_entropy_vs_n_from_Hlower(H_lower)

    

