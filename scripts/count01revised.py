from pathlib import Path

data_dir = Path(r"E:\Project\MLDSA\RO_TRNG\data\lutl")
output_file = Path(r"E:\Project\MLDSA\RO_TRNG\data\lutl\count01_results.txt")

files = sorted(data_dir.glob("RO*.DAT"))

if not files:
    print("没有找到 RO*.DAT 文件")
    raise SystemExit

results = []

for file_path in files:
    with open(file_path, "rb") as f:
        data = f.read()

    total_bits = len(data) * 8
    ones = sum(bin(byte).count("1") for byte in data)
    zeros = total_bits - ones
    p = ones / total_bits if total_bits else 0

    result = (
        f"{file_path.name}: "
        f"bytes={len(data)}, "
        f"bits={total_bits}, "
        f"zeros={zeros}, "
        f"ones={ones}, "
        f"p={p:.6f}"
    )
    print(result)
    results.append(result)

with open(output_file, "w", encoding="utf-8") as f:
    for line in results:
        f.write(line + "\n")

print(f"\n结果已保存到: {output_file}")
