""" 绘制变换前后的嵌套网络 """

import numpy as np
import matplotlib.pyplot as plt

y_lines = []
n = 512 # 线段上的点数，越多越精确

y_min, y_max = -3, 3
y_hole_max = (y_max - y_min) * 0.25
y_hole_min = - y_hole_max

# 竖线
for i in np.linspace(y_min, y_max, 17):
    # 中间断开画
    if y_hole_min <= i <= y_hole_max:
        x = np.full(n//4+1, i)
        
        y = np.linspace(y_min, y_hole_min, n//4+1)
        y_lines.append([x, y])
        
        y = np.linspace(y_hole_max, y_max, n//4+1)
        y_lines.append([x, y])
    else:
        x = np.full(n+1, i)
        y = np.linspace(y_min, y_max, n+1)
        y_lines.append([x, y])

# 水平线，从竖线旋转而来 x = -y，y = x
x_lines = []
for line in y_lines:
    x_line = [-line[1], line[0]]
    x_lines.append(x_line)

# 转为 numpy 数组，方便运算
y_lines = [np.array(line) for line in y_lines]
x_lines = [np.array(line) for line in x_lines]

# 常数
z0 = 0 + 4j
c = 2*np.pi*1j / (np.log(16) + 2*np.pi*1j)

# 颜色
pastel_rainbow = [
    'tomato',
    'sandybrown',
    'gold',
    'darkseagreen',
    'skyblue',
    'slateblue',
    'orchid',
] * 2

# 绘图
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10,5))

# 嵌套绘制
for color in pastel_rainbow:
    # 左图：原图
    for x, y in y_lines + x_lines:
        ax1.plot(x, y, '.', markersize=0.1, c=color)

    # 右图：复变换后
    for x, y in y_lines + x_lines:
        z = x + y*1j
        z_new = np.log(z)
        z_new = c * (z_new - z0) + z0
        z_new = np.exp(z_new)
        ax2.plot(z_new.real, z_new.imag, '.', markersize=0.1, c=color)
    
    # 缩小一倍继续绘制
    y_lines = [line/2 for line in y_lines]
    x_lines = [line/2 for line in x_lines]

# 设置坐标轴范围和比例
for ax in [ax1, ax2]:
    ax.set(xlim=(-3, 3), ylim=(-3, 3), aspect='equal')

plt.tight_layout()
plt.show()