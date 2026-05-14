from pathlib import Path
from collections import Counter
import math
import matplotlib.pyplot as plt

# ====== 你只需要改这里 ======
DATA_DIR = Path(r"E:\Project\MLDSA\RO_TRNG\data\lutl")
OUTPUT_DIR = Path(r"E:\Project\MLDSA\RO_TRNG\data\zynq7020_compare_20260415")
FILE_GLOB = "RO*.DAT"
# ===========================


def shannon_entropy_from_bytes(data: bytes) -> float:
    if not data:
        return 0.0
    total = len(data)
    counter = Counter(data)
    probs = [count / total for count in counter.values()]
    return -sum(p * math.log2(p) for p in probs if p > 0)


def min_entropy_from_bytes(data: bytes) -> float:
    if not data:
        return 0.0
    total = len(data)
    counter = Counter(data)
    max_p = max(counter.values()) / total
    return -math.log2(max_p)


def bit_bias_stats(data: bytes):
    total_bits = len(data) * 8
    ones = sum(byte.bit_count() for byte in data)
    zeros = total_bits - ones
    p1 = ones / total_bits if total_bits else 0.0
    return zeros, ones, total_bits, p1


def ensure_dirs():
    (OUTPUT_DIR / "result").mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "fig").mkdir(parents=True, exist_ok=True)


def save_text(results):
    out_file = OUTPUT_DIR / "result" / "summary.txt"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(
            "file\tbytes\tbits\tzeros\tones\tp1\tshannon_entropy_byte\tmin_entropy_byte\n"
        )
        for r in results:
            f.write(
                f"{r['name']}\t{r['bytes']}\t{r['bits']}\t{r['zeros']}\t{r['ones']}\t"
                f"{r['p1']:.6f}\t{r['shannon_byte']:.6f}\t{r['min_byte']:.6f}\n"
            )
    return out_file


def plot_metric(results, key, title, ylabel, filename):
    names = [r["name"].replace(".DAT", "") for r in results]
    values = [r[key] for r in results]

    plt.figure(figsize=(10, 5))
    plt.bar(names, values)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.grid(True, axis="y", linestyle="--", alpha=0.4)
    plt.tight_layout()
    out_path = OUTPUT_DIR / "fig" / filename
    plt.savefig(out_path, dpi=150)
    plt.close()
    return out_path


def main():
    ensure_dirs()
    files = sorted(DATA_DIR.glob(FILE_GLOB))

    if not files:
        print(f"没有找到文件: {DATA_DIR / FILE_GLOB}")
        return

    results = []
    print(
        f"{'file':<10} {'bytes':>10} {'p1':>10} {'Shannon(byte)':>16} {'MinEntropy(byte)':>18}"
    )
    print("-" * 70)

    for path in files:
        data = path.read_bytes()
        zeros, ones, bits, p1 = bit_bias_stats(data)
        shannon_byte = shannon_entropy_from_bytes(data)
        min_byte = min_entropy_from_bytes(data)

        result = {
            "name": path.name,
            "bytes": len(data),
            "bits": bits,
            "zeros": zeros,
            "ones": ones,
            "p1": p1,
            "shannon_byte": shannon_byte,
            "min_byte": min_byte,
        }
        results.append(result)

        print(
            f"{path.name:<10} {len(data):>10} {p1:>10.6f} "
            f"{shannon_byte:>16.6f} {min_byte:>18.6f}"
        )

    text_path = save_text(results)
    fig1 = plot_metric(results, "p1", "Bit-1 Ratio p(1)", "p(1)", "p1_ratio.png")
    fig2 = plot_metric(
        results,
        "shannon_byte",
        "Shannon Entropy per Byte",
        "bits",
        "shannon_entropy_byte.png",
    )
    fig3 = plot_metric(
        results,
        "min_byte",
        "Min-Entropy per Byte",
        "bits",
        "min_entropy_byte.png",
    )

    print("\n结果已保存：")
    print(text_path)
    print(fig1)
    print(fig2)
    print(fig3)


if __name__ == "__main__":
    main()
