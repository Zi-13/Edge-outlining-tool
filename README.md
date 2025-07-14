# Edge-outlining-tool
A tool for performing Fourier series fitting (in trigonometric form) to the boundaries of specific locations on a map
这是一个给地图上特定地点描边和傅里叶拟合的小工具
DrawTheEdge.py 使用说明
功能简介
自动提取图片中目标颜色区域，检测所有色块并描边。
对每个色块进行傅里叶级数拟合，平滑轮廓。
支持鼠标点击或键盘左右键切换选中色块。
选中色块时，界面下方实时显示色块编号、面积、周长等属性。
右侧专门显示当前选中色块的放大视图。
依赖环境
Python 3.7 及以上
OpenCV (cv2)
numpy
matplotlib
安装依赖：
pip install opencv-python numpy matplotlib
使用方法
修改 main() 函数中的图片路径为你要处理的图片：
pick_color_and_draw_edge('你的图片路径.png', order=80)
运行脚本：
按提示在弹出的窗口中点击目标色块区域，选取颜色后关闭窗口。
程序会自动检测所有色块并显示交互界面：
左图：颜色提取结果
中图：所有色块的傅里叶拟合轮廓
右图：当前选中色块的放大视图
下方红色文字：显示当前色块编号、面积、周长
交互操作：
鼠标点击中图或右图的色块，可选中并高亮该色块
键盘左右方向键可切换选中色块
说明
面积和周长均为像素级，基于原始轮廓点计算。
傅里叶拟合仅用于平滑和可视化，不影响面积计算。
若色块较多，图例会自动隐藏，线宽自动调整。
常见问题
图片无法读取：请检查图片路径是否正确。
没有色块被检测到：请确保选取的颜色区域在图片中存在。
依赖未安装：请先运行 pip install 安装依赖。

这个整体基于我的高数作业，但实际用起来我觉得拟合这步好像没那么必要，所以又加了一个没有傅里叶的版本就是_withooutfourier的版本，还加上了染色
后续可能会加上比例尺计算面积吧-20257.14
