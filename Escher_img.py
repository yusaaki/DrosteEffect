""" 本脚本 可以基于 带嵌套的 有德罗斯特效果的 正方形图片 通过 坐标变换 进而 生成 无限螺旋递归的 和 埃舍尔画作《画廊》类似的 视觉效果的 图片 """
""" 参考了 3Blue1Brown 的视频 https://www.bilibili.com/video/BV1779MBHESt How (and why) to take a logarithm of an image """

import cv2
import numpy as np
import matplotlib.pyplot as plt

def Droste(img, ratio, n_iter=8):
    # 检查图片尺寸
    img_h, img_w = img.shape[:2]
    print(f"图片尺寸：{img_w} x {img_h}")
    if img_h != img_w:
        print("图片需为正方形")
        exit()

    # 计算图像中央嵌套区域的像素坐标
    center_x, center_y = img_w // 2, img_h // 2
    rect_len = img_h // ratio # 嵌套区域边长
    rect_x1 = center_x - rect_len // 2
    rect_x2 = center_x + rect_len // 2
    rect_y1 = center_y - rect_len // 2
    rect_y2 = center_y + rect_len // 2
    print(f"嵌套区域像素坐标: 左上 ({rect_x1},{rect_y1}) 右下 ({rect_x2},{rect_y2})")
    
    # 构建目标图像的几何坐标 x_t, y_t
    x_min, x_max = -3.0, 3.0 # 准备把原图从像素坐标投到几何坐标上的这个范围
    y_min, y_max = -3.0, 3.0
    x_t = np.linspace(x_min, x_max, img_w)
    y_t = np.linspace(y_max, y_min, img_h) # 从上到下递减
    x_t, y_t = np.meshgrid(x_t, y_t)
    z_t = x_t + 1j * y_t
    
    # 利用逆变换，从目标图像的几何坐标 x_t, y_t 反向计算得到原图像坐标 x_s, y_s
    # 常数
    z0 = 1 + 4j # 这个点是原图某个点的几何坐标经过 z = ln(z) 变换之后的复数坐标
    c = 2 * np.pi * 1j / (np.log(ratio) + 2 * np.pi * 1j)
    # 逆变换
    z_s = np.exp(z0 + (np.log(z_t) - z0) / c) # 如果是恒等变换: z_s = z_t，就是普通的德罗斯特效果
    x_s = np.real(z_s)
    y_s = np.imag(z_s)
    
    # 将源图像几何坐标 x_s, y_s 线性映射到原图像素坐标 x_s_img, y_s_img
    x_s_img = (x_s - x_min) / (x_max - x_min) * img_w
    y_s_img = (y_max - y_s) / (y_max - y_min) * img_h
    x_s_img = np.clip(x_s_img, 0, img_w - 1) # 这里对于超出范围的点不应重新裁剪，而是再向外套一层，懒得写了
    y_s_img = np.clip(y_s_img, 0, img_h - 1)
    
    # 迭代，将落在中间嵌套区域中的点映射到原图
    for i in range(n_iter):
        # 找出落在嵌套区域内的像素点
        mask = (x_s_img >= rect_x1) & (x_s_img <= rect_x2) & (y_s_img >= rect_y1) & (y_s_img <= rect_y2)
        if not np.any(mask):
            print("迭代完成，迭代次数：", i, "次")
            break
        
        # 对范围内的点，利用其像素坐标，计算其在区域内的相对位置，用 0 ~ 1 表示，(u, v) ∈ [0,1]
        u = (x_s_img[mask] - rect_x1) / (rect_x2 - rect_x1)
        v = (y_s_img[mask] - rect_y1) / (rect_y2 - rect_y1)
        
        # 将相对位置线性映射到原图的像素坐标
        x_s_img_new = u * img_w
        y_s_img_new = v * img_h
        x_s_img_new = np.clip(x_s_img_new, 0, img_w - 1)
        y_s_img_new = np.clip(y_s_img_new, 0, img_h - 1)
        
        # 更新这些点的映射坐标
        x_s_img[mask] = x_s_img_new
        y_s_img[mask] = y_s_img_new

    # 5. 根据最终的映射坐标从原图中采样
    x_s_img = x_s_img.astype(np.float32)
    y_s_img = y_s_img.astype(np.float32)
    result = cv2.remap(img, x_s_img, y_s_img, interpolation=cv2.INTER_NEAREST)
    return result


if __name__ == "__main__":
    # 读入图像
    img_path = r".\img.png"
    img = cv2.imread(img_path)
    
    if img is None:
        raise FileNotFoundError(f"图片读取失败: {img_path}")
    
    result = Droste(img, ratio=4)
    cv2.imwrite(r".\droste_result.png", result)
    result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
    
    plt.figure(figsize=(7, 7))
    plt.imshow(result, extent=[-3, 3, -3, 3])
    plt.tight_layout()
    plt.show()