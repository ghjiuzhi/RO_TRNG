# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif']='SimHei'
plt.rcParams['font.size'] = 14  # 设置全局默认字体大小

# 假设你的数据如下（请替换为你的真实数据）
# 每个 RO 级别有4个数量点，对应的X是数量，Y是测量值
ro_data = {
    'RO-1': {'x': [4, 8, 16], 'y': [0.618689, 0.853576, 0.866127]},
    'RO-2': {'x': [4, 8, 16], 'y': [0.809859, 0.826460, 0.823033]},
    'RO-3': {'x': [4, 8, 16], 'y': [0.365922, 0.914415, 0.899422]},
    'RO-4': {'x': [4, 8, 16], 'y': [0.803960, 0.868389, 0.872136]},
}

# 绘图
plt.figure(figsize=(10, 6))

for ro_level, data in ro_data.items():
    x = np.array(data['x'])
    y = np.array(data['y'])
    
    # 直接绘制折线图
    plt.plot(x, y, marker='o', label=ro_level, linewidth=2)

plt.title('F7MUX RO数量与最小熵关系', fontsize=19)
plt.xlabel('RO数量', fontsize=17)
plt.ylabel('最小熵', fontsize=17)
plt.legend(fontsize=14)
plt.grid(True)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.tight_layout()
plt.show()
