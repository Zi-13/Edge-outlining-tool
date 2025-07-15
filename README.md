# Edge Outlining Tool

A tool for performing Fourier series fitting (in trigonometric form) to the boundaries of specific locations on a map.  
这是一个用于地图上特定地点描边和傅里叶拟合的小工具。

---

## 功能简介  
## Features

- 自动提取图片中目标颜色区域，检测所有色块并描边。  
  Automatically extracts target color regions in the image, detects all color blocks, and outlines them.
- 对每个色块进行傅里叶级数拟合，实现轮廓平滑。  
  Performs Fourier series fitting for each color block to smooth the contour.
- 支持鼠标点击或键盘左右键切换选中色块。  
  Supports selecting color blocks by mouse click or using left/right arrow keys.
- 实时显示选中色块的编号、面积、周长等属性。  
  Displays the ID, area, perimeter, and other attributes of the selected color block in real time.
- 右侧专门显示当前选中色块的放大视图。  
  Shows a zoomed-in view of the current selected color block on the right.

---

## 依赖环境  
## Requirements

- Python 3.7 及以上  
  Python 3.7 or higher
- OpenCV (`cv2`)
- `numpy`
- `matplotlib`

### 安装依赖  
### Installation

```bash
pip install opencv-python numpy matplotlib
```

---

## 使用方法  
## Usage

1. 修改 `main()` 函数中的图片路径为你要处理的图片：  
   Modify the image path in the `main()` function to your target image:

    ```python
    pick_color_and_draw_edge('你的图片路径.png', order=80)
    ```

2. 运行脚本：  
   Run the script:

    - 按提示在弹出的窗口中点击目标色块区域，选取颜色后关闭窗口。  
      Follow the prompt to click on the target color area in the pop-up window, then close the window after selecting the color.
    - 程序会自动检测所有色块并显示交互界面：  
      The program will automatically detect all color blocks and display an interactive interface:
        - 左图：颜色提取结果  
          Left: Color extraction result
        - 中图：所有色块的傅里叶拟合轮廓  
          Middle: Fourier-fitted outlines of all color blocks
        - 右图：当前选中色块的放大视图  
          Right: Zoomed-in view of the current selected color block
        - 下方红色文字：当前色块编号、面积、周长  
          Red text below: current color block index, area, and perimeter

---

## 交互操作  
## Interaction

- 鼠标点击中图或右图的色块，可选中并高亮该色块。  
  Click on a color block in the middle or right image to select and highlight it.
- 键盘左右方向键可切换选中色块。  
  Use the left or right arrow keys to switch the selected color block.

---

## 说明  
## Notes

- 面积和周长均为像素级，基于原始轮廓点计算。  
  Both area and perimeter are measured in pixels, calculated from the original contour points.
- 傅里叶拟合仅用于平滑和可视化，不影响面积计算。  
  Fourier fitting is only for smoothing and visualization, and does not affect area calculation.
- 若色块较多，图例会自动隐藏，线宽自动调整。  
  When there are too many color blocks, the legend will automatically hide, and line width will adjust automatically.

---

## 常见问题  
## FAQ

- **图片无法读取**：请检查图片路径是否正确。  
  **Image cannot be read**: Please check if the image path is correct.
- **没有色块被检测到**：请确保选取的颜色区域在图片中存在。  
  **No color block detected**: Please ensure the selected color region exists in the image.
- **依赖未安装**：请先运行 `pip install` 安装依赖。  
  **Dependencies not installed**: Please run `pip install` to install the dependencies.

---

## 关于这个项目  
## About This Project

- 本工具最初基于高数作业开发，实际使用时发现傅里叶拟合并非必需，因此提供了不带傅里叶拟合的 `_withooutfourier` 版本，并增加了染色功能。  
  This tool was initially developed for a calculus assignment. In practice, Fourier fitting was found to be unnecessary, so a `_withooutfourier` version without Fourier fitting and with coloring features was added.
- 后续可能会增加比例尺用于面积计算。（2025.7.14）  
  In the future, a scale feature may be added for area calculation. (2025.7.14)

---
