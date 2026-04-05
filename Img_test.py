""" 生成带网格的测试图片 """

from PIL import Image, ImageDraw, ImageFont, ImageColor
import os

# 图片参数
img_size = 4096
grid_count = 16
cell_size = img_size // grid_count  # 128

# 创建图像
img = Image.new("RGB", (img_size, img_size), "white")
draw = ImageDraw.Draw(img)

# 绘制格子
for row in range(grid_count):
    for col in range(grid_count):
        x0 = col * cell_size
        y0 = row * cell_size
        # 彩色格子
        if (row + col) % 2 == 0:
            # 计算色相
            t = (row + col) / (2 * (grid_count - 1))
            hue = t * 360
            # 用 HSV 生成纯彩虹色（饱和度70%，亮度90%）
            color = ImageColor.getrgb(f"hsv({int(hue)}, 70%, 90%)")
            draw.rectangle([x0, y0, x0+cell_size, y0+cell_size], fill=color)
        # 白色格子
        else:
            draw.rectangle([x0, y0, x0+cell_size, y0+cell_size], fill="white")

# 使用默认字体
font_size = int(cell_size * 0.4)
try:
    font = ImageFont.truetype("arial.ttf", font_size)
except:
    font = ImageFont.load_default()

# 写数字
num = 1
for row in range(grid_count):
    for col in range(grid_count):
        cx = col * cell_size + cell_size // 2
        cy = row * cell_size + cell_size // 2
        # 根据格子背景色决定文字颜色
        color = "white" if (row + col) % 2 == 0 else "black"
        draw.text((cx, cy), str(num), fill=color, font=font, anchor="mm")
        num += 1

# 保存
img.save(r".\img.png")