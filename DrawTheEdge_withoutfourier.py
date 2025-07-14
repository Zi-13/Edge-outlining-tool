import cv2
import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import lstsq
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 黑体
matplotlib.rcParams['axes.unicode_minus'] = False

def fit_fourier_series(data, t, order):
    A = np.ones((len(t), 2 * order + 1))
    for k in range(1, order + 1):
        A[:, 2 * k - 1] = np.cos(k * t)
        A[:, 2 * k] = np.sin(k * t)
    coeffs, _, _, _ = lstsq(A, data, rcond=None)
    return coeffs

def evaluate_fourier_series(coeffs, t, order):
    A = np.ones((len(t), 2 * order + 1))
    for k in range(1, order + 1):
        A[:, 2 * k - 1] = np.cos(k * t)
        A[:, 2 * k] = np.sin(k * t)
    return A @ coeffs

def fourier_fit_and_plot(points, order, label='傅里叶拟合轮廓', linewidth=1.2):
    try:
        x = points[:, 0]
        y = points[:, 1]
        N = len(points)
        t = np.linspace(0, 2 * np.pi, N)
        coeffs_x = fit_fourier_series(x, t, order)
        coeffs_y = fit_fourier_series(y, t, order)
        x_fit = evaluate_fourier_series(coeffs_x, t, order)
        y_fit = evaluate_fourier_series(coeffs_y, t, order)
        plt.plot(x, y, 'k.', markersize=1, alpha=0.3)  # 原始点淡化
        plt.plot(x_fit, y_fit, '-', linewidth=linewidth, label=label)
    except Exception as e:
        print(f"[傅里叶拟合失败]：{e}")

def pick_color_and_draw_edge(image_path):
    img = cv2.imread(image_path)
    if img is None:
        print("图片读取失败")
        return
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    picked = []
    def on_mouse(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            color = hsv[y, x]
            print(f"选中点HSV: {color}")
            picked.append(color)
    cv2.imshow("点击选取目标区域颜色", img)
    cv2.setMouseCallback("点击选取目标区域颜色", on_mouse)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    if not picked:
        print("未选取颜色")
        return
    hsv_arr = np.array(picked)
    h, s, v = np.mean(hsv_arr, axis=0).astype(int)
    print(f"HSV picked: {h}, {s}, {v}")
    lower = np.array([max(h-15,0), max(s-60,0), max(v-60,0)])
    upper = np.array([min(h+15,179), min(s+60,255), min(v+60,255)])
    print(f"lower: {lower}, upper: {upper}")
    mask = cv2.inRange(hsv, lower, upper)
    color_extract = cv2.bitwise_and(img, img, mask=mask)
    # --- 记录所有有效轮廓及属性 ---
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    valid_contours = []
    for i, contour in enumerate(contours):
        if contour.shape[0] < 20:
            continue
        area = cv2.contourArea(contour)
        length = cv2.arcLength(contour, True)
        valid_contours.append({
            'contour': contour,
            'points': contour[:, 0, :],
            'area': area,
            'length': length,
            'idx': i
        })
    n_contours = len(valid_contours)
    linewidth = max(0.5, 2 - 0.03 * n_contours)
    show_legend = n_contours <= 15
    # --- 交互式显示 ---
    fig, axes = plt.subplots(1, 3, figsize=(16, 6))
    ax_img, ax_fit, ax_zoom = axes
    ax_img.set_title("颜色提取结果")
    ax_img.imshow(cv2.cvtColor(color_extract, cv2.COLOR_BGR2RGB))
    ax_img.axis('off')
    ax_fit.set_title("轮廓显示")
    ax_fit.axis('equal')
    ax_fit.invert_yaxis()
    ax_fit.grid(True)
    ax_zoom.set_title("色块放大视图")
    ax_zoom.axis('equal')
    ax_zoom.grid(True)
    selected_idx = [0]  # 用列表包裹以便闭包修改
    info_text = None
    def draw_all(highlight_idx=None):
        ax_fit.clear()
        ax_fit.set_title("轮廓显示")
        ax_fit.axis('equal')
        ax_fit.invert_yaxis()
        ax_fit.grid(True)
        
        # 准备颜色列表
        colors = plt.cm.tab10(np.linspace(0, 1, max(len(valid_contours), 10)))
        
        for j, info in enumerate(valid_contours):
            points = info['points']
            label = f"色块{info['idx']+1}"
            
            if highlight_idx is not None and j == highlight_idx:
                fill_color = 'red'
                edge_color = 'darkred'
                lw = linewidth * 2
                alpha = 0.7
                zorder = 10
            else:
                fill_color = colors[j % len(colors)]
                edge_color = 'black'
                lw = linewidth
                alpha = 0.5
                zorder = 1
            
            x = points[:, 0]
            y = points[:, 1]
            
            # 填充色块区域
            ax_fit.fill(x, y, color=fill_color, alpha=alpha, zorder=zorder, label=label if show_legend else None)
            # 绘制轮廓边界
            ax_fit.plot(x, y, '-', color=edge_color, linewidth=lw, zorder=zorder+1)
            
        if show_legend:
            ax_fit.legend()
        # --- 属性信息显示在右图下方 ---
        info = valid_contours[highlight_idx if highlight_idx is not None else 0]
        ax_fit.text(0.02, -0.12, f"色块编号: {info['idx']+1}  面积: {info['area']:.2f}  周长: {info['length']:.2f}",
                    transform=ax_fit.transAxes, fontsize=12, color='red', va='top')
        # --- 放大视图 ---
        ax_zoom.clear()
        ax_zoom.set_title("色块放大视图")
        ax_zoom.axis('equal')
        ax_zoom.invert_yaxis()
        ax_zoom.grid(True)
        points = info['points']
        x = points[:, 0]
        y = points[:, 1]
        
        # 在放大视图中也显示填充
        if highlight_idx is not None:
            fill_color = 'red'
            alpha = 0.7
        else:
            fill_color = colors[0 % len(colors)]
            alpha = 0.5
            
        # 填充区域
        ax_zoom.fill(x, y, color=fill_color, alpha=alpha, label='填充区域')
        # 绘制轮廓点和连线
        ax_zoom.plot(x, y, 'k.', markersize=2, alpha=0.8, label='轮廓点')
        ax_zoom.plot(x, y, 'black', linewidth=2, label='轮廓线')
        ax_zoom.legend()
        # 自适应缩放
        margin = 20
        ax_zoom.set_xlim(x.min()-margin, x.max()+margin)
        ax_zoom.set_ylim(y.min()-margin, y.max()+margin)
        fig.canvas.draw_idle()
    def show_info(idx):
        # 已集成到draw_all中，无需单独显示
        pass
    def on_click(event):
        if event.inaxes not in [ax_img, ax_fit, ax_zoom]:
            return
        x, y = int(event.xdata), int(event.ydata)
        found = False
        for j, info in enumerate(valid_contours):
            if cv2.pointPolygonTest(info['contour'], (x, y), False) >= 0:
                selected_idx[0] = j
                draw_all(highlight_idx=j)
                found = True
                break
        if not found:
            print("未选中任何色块")
    def on_key(event):
        if event.key == 'right':
            selected_idx[0] = (selected_idx[0] + 1) % n_contours
            draw_all(highlight_idx=selected_idx[0])
        elif event.key == 'left':
            selected_idx[0] = (selected_idx[0] - 1) % n_contours
            draw_all(highlight_idx=selected_idx[0])
    draw_all(highlight_idx=selected_idx[0])
    fig.canvas.mpl_connect('button_press_event', on_click)
    fig.canvas.mpl_connect('key_press_event', on_key)
    plt.tight_layout()
    plt.show()

def main():
    pick_color_and_draw_edge('c:\\Users\\Jason\\Desktop\\JustForTry.png') 
if __name__ == "__main__":
    main()
