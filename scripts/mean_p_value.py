def calculate_average(data):
    if not data:
        return None  # 或 raise ValueError("数据列表为空")
    return sum(data) / len(data)

# 示例数据（替换为你的数据）
float_data = [0.437274, 0.739918]

average = calculate_average(float_data)
print(f"平均数是: {average}")
