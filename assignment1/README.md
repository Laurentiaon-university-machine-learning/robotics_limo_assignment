# AprilTag Detection System | AprilTag检测系统

**English** | [中文](#中文版本)

An OpenCV-based AprilTag detection system optimized for 8-10cm traffic sign markers, featuring real-time distance measurement and dynamic focal length calibration.

一个基于OpenCV的AprilTag检测系统，专门针对8-10cm交通标志标记进行优化，具有实时距离测量和动态焦距校准功能。

## Features | 功能特性

- 🎯 **High-Precision Detection**: Optimized detection parameters for 8-10cm AprilTag markers | **高精度检测**：针对8-10cm AprilTag标记优化的检测参数
- 📏 **Distance Measurement**: Real-time calculation of marker-to-camera distance | **距离测量**：实时计算标记到摄像头的距离
- 🔧 **Dynamic Calibration**: Real-time focal length adjustment for improved accuracy | **动态校准**：支持实时调整焦距参数以提高测量精度
- 👁️ **Image Processing Visualization**: Complete image processing pipeline display | **图像处理可视化**：显示完整的图像处理流程
- 🚦 **Traffic Sign Recognition**: Support for 6 types of traffic signs | **交通标志识别**：支持6种交通标志类型识别
- ⏱️ **Smart Stop Logic**: 3-second stop execution when STOP sign detected | **智能停车逻辑**：检测到STOP标志时执行3秒停车逻辑

## Supported Traffic Signs | 支持的交通标志

| ID | Sign Type | Description | 标志类型 | 描述 |
|----|-----------|-------------|----------|------|
| 0  | NO ENTRY | No Entry | 禁止通行 | 禁止通行 |
| 1  | DEAD END | Dead End | 死路 | 死路 |
| 2  | TURN RIGHT | Turn Right | 右转 | 右转 |
| 3  | TURN LEFT | Turn Left | 左转 | 左转 |
| 4  | FORWARD | Go Forward | 直行 | 直行 |
| 5  | STOP | Stop | 停车 | 停车 |

## System Requirements | 系统要求

- Python 3.7+ | Python 3.7+
- OpenCV 4.0+ | OpenCV 4.0+
- NumPy | NumPy
- Camera device | 摄像头设备

## Installation | 安装

1. Clone the repository | 克隆项目：
```bash
git clone <repository-url>
cd robotic_assignment
```

2. Install dependencies | 安装依赖：
```bash
pip install -r requirements.txt
```

3. Run the program | 运行程序：
```bash
cd assignment1
python aprilTag_detect.py
```

## Usage Instructions | 使用说明

### Basic Controls | 基本操作

| Key | Function | 按键 | 功能 |
|-----|----------|------|------|
| **ESC** | Exit program | **ESC** | 退出程序 |
| **S** | Save processing steps | **S** | 保存图像处理步骤 |
| **↑** or **W** | Increase focal length | **↑** 或 **W** | 增加焦距（距离显示增加） |
| **↓** or **D** | Decrease focal length | **↓** 或 **D** | 减少焦距（距离显示减少） |
| **R** | Reset focal length to default (1000) | **R** | 重置焦距为默认值(1000) |
| **C** | Show calibration instructions | **C** | 显示校准说明 |

### Focal Length Calibration Steps | 焦距校准步骤

1. Place AprilTag markers at known distances (recommended: 30cm, 50cm, 100cm) | 将AprilTag标记放在已知距离处（推荐30cm、50cm、100cm）
2. Observe the displayed distance values | 观察屏幕显示的距离值
3. Adjust based on deviation | 根据偏差调整：
   - Displayed distance **less than** actual distance → Press **↑** or **W** to increase focal length | 显示距离**小于**实际距离 → 按 **↑** 或 **W** 增加焦距
   - Displayed distance **greater than** actual distance → Press **↓** or **D** to decrease focal length | 显示距离**大于**实际距离 → 按 **↓** 或 **D** 减少焦距
4. Repeat adjustment until displayed distance approaches actual distance | 重复调整直到显示距离接近实际距离
5. Press **R** to reset to default value anytime | 按 **R** 可随时重置为默认值

### Window Description | 窗口说明

The program displays two windows when running | 程序运行时会显示两个窗口：

1. **Main Detection Window | 主检测窗口**：
   - Real-time camera feed | 实时摄像头画面
   - AprilTag detection results and borders | AprilTag检测结果和边框
   - Distance information and traffic sign types | 距离信息和交通标志类型
   - FPS and system status information | FPS和系统状态信息

2. **Image Processing Steps Window | 图像处理步骤窗口**：
   - Original grayscale image | 原始灰度图
   - After Gaussian blur processing | 高斯模糊处理后
   - After CLAHE contrast enhancement | CLAHE对比度增强后
   - After adaptive threshold binarization | 自适应阈值二值化后

## Technical Details | 技术细节

### Detection Parameter Optimization | 检测参数优化

Optimized parameters for 8-10cm markers | 针对8-10cm标记的优化参数：
- `minMarkerPerimeterRate`: 0.02 (suitable for small markers) | 0.02 (适合小尺寸标记)
- `adaptiveThreshWinSizeMin/Max`: 3-23 (multi-scale threshold) | 3-23 (多尺度阈值)
- `cornerRefinementMethod`: Sub-pixel corner refinement | 亚像素级角点精化

### Image Preprocessing Pipeline | 图像预处理流程

1. **Color to Grayscale Conversion | 彩色到灰度转换**
2. **Gaussian Blur** (3x3 kernel, noise reduction) | **高斯模糊** (3x3核，减少噪声)
3. **CLAHE Contrast Enhancement** (clipLimit=3.0) | **CLAHE对比度增强** (clipLimit=3.0)
4. **Adaptive Threshold Processing | 自适应阈值处理**

### Distance Calculation Formula | 距离计算公式

**English:**
```
Distance(cm) = (Marker Actual Width × Focal Length) / Pixel Width
```

**中文:**
```
距离(cm) = (标记实际宽度 × 焦距) / 像素宽度
```

- Marker actual width: 9.0cm (average of 8-10cm markers) | 标记实际宽度：9.0cm (8-10cm标记平均值)
- Focal length: Default 1000, dynamically adjustable | 焦距：默认1000，可动态调节
- Pixel width: Detected marker size in pixels | 像素宽度：检测到的标记在图像中的像素尺寸

## File Structure | 文件结构

```
robotic_assignment/
├── README.md                 # Project documentation | 项目说明文档
├── .gitignore               # Git ignore configuration | Git忽略文件配置
├── requirements.txt         # Python dependencies | Python依赖包列表
└── assignment1/
    └── aprilTag_detect.py   # Main program file | 主程序文件
```

## Troubleshooting | 故障排除

### Common Issues | 常见问题

1. **Camera Cannot Open | 摄像头无法打开**
   - Check if camera is occupied by other programs | 检查摄像头是否被其他程序占用
   - Try changing camera ID (VideoCapture parameter) | 尝试更改摄像头ID (VideoCapture参数)

2. **Low Detection Accuracy | 检测精度不高**
   - Ensure good lighting conditions | 确保光照条件良好
   - Adjust camera focus and angle | 调整摄像头焦距和角度
   - Use focal length calibration function | 使用焦距校准功能

3. **Inaccurate Distance Measurement | 距离测量不准确**
   - Press **C** to view calibration instructions | 按 **C** 查看校准说明
   - Use known distance markers for calibration | 使用已知距离的标记进行校准
   - Adjust focal length parameters | 调整焦距参数

4. **Arrow Keys Not Responding | 箭头键无响应**
   - Use backup keys **W/D** | 使用备用按键 **W/D**
   - Check terminal output for key values for debugging | 检查终端输出的按键值进行调试

## Development Information | 开发信息

- **Programming Language | 开发语言**: Python
- **Main Dependencies | 主要依赖**: OpenCV, NumPy
- **AprilTag Dictionary | AprilTag字典**: DICT_APRILTAG_36h11
- **Supported Platforms | 支持平台**: Windows, macOS, Linux

## Contributing | 贡献

Welcome to submit Issues and Pull Requests to improve this project.

欢迎提交Issue和Pull Request来改进这个项目。

## License | 许可证

This project is licensed under the MIT License. See LICENSE file for details.

本项目采用MIT许可证。详见LICENSE文件。

---

# 中文版本

[English](#apriltag-detection-system--apriltag检测系统) | **中文**

## 功能特性

- 🎯 **高精度检测**：针对8-10cm AprilTag标记优化的检测参数
- 📏 **距离测量**：实时计算标记到摄像头的距离
- 🔧 **动态校准**：支持实时调整焦距参数以提高测量精度
- 👁️ **图像处理可视化**：显示完整的图像处理流程
- 🚦 **交通标志识别**：支持6种交通标志类型识别
- ⏱️ **智能停车逻辑**：检测到STOP标志时执行3秒停车逻辑

## 支持的交通标志

| ID | 标志类型 | 描述 |
|----|----------|------|
| 0  | NO ENTRY | 禁止通行 |
| 1  | DEAD END | 死路 |
| 2  | TURN RIGHT | 右转 |
| 3  | TURN LEFT | 左转 |
| 4  | FORWARD | 直行 |
| 5  | STOP | 停车 |

## 系统要求

- Python 3.7+
- OpenCV 4.0+
- NumPy
- 摄像头设备

## 安装步骤

1. 克隆项目：
```bash
git clone <repository-url>
cd robotic_assignment
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 运行程序：
```bash
cd assignment1
python aprilTag_detect.py
```

## 详细使用说明

### 按键操作

| 按键 | 功能 |
|------|------|
| **ESC** | 退出程序 |
| **S** | 保存图像处理步骤 |
| **↑** 或 **W** | 增加焦距（距离显示增加） |
| **↓** 或 **D** | 减少焦距（距离显示减少） |
| **R** | 重置焦距为默认值(1000) |
| **C** | 显示校准说明 |

### 焦距校准步骤

1. 将AprilTag标记放在已知距离处（推荐30cm、50cm、100cm）
2. 观察屏幕显示的距离值
3. 根据偏差调整：
   - 显示距离**小于**实际距离 → 按 **↑** 或 **W** 增加焦距
   - 显示距离**大于**实际距离 → 按 **↓** 或 **D** 减少焦距
4. 重复调整直到显示距离接近实际距离
5. 按 **R** 可随时重置为默认值

### 窗口说明

程序运行时会显示两个窗口：

1. **主检测窗口**：
   - 实时摄像头画面
   - AprilTag检测结果和边框
   - 距离信息和交通标志类型
   - FPS和系统状态信息

2. **图像处理步骤窗口**：
   - 原始灰度图
   - 高斯模糊处理后
   - CLAHE对比度增强后
   - 自适应阈值二值化后

## 技术细节

### 检测参数优化

针对8-10cm标记的优化参数：
- `minMarkerPerimeterRate`: 0.02 (适合小尺寸标记)
- `adaptiveThreshWinSizeMin/Max`: 3-23 (多尺度阈值)
- `cornerRefinementMethod`: 亚像素级角点精化

### 图像预处理流程

1. **彩色到灰度转换**
2. **高斯模糊** (3x3核，减少噪声)
3. **CLAHE对比度增强** (clipLimit=3.0)
4. **自适应阈值处理**

### 距离计算公式

```
距离(cm) = (标记实际宽度 × 焦距) / 像素宽度
```

- 标记实际宽度：9.0cm (8-10cm标记平均值)
- 焦距：默认1000，可动态调节
- 像素宽度：检测到的标记在图像中的像素尺寸

## 故障排除

### 常见问题

1. **摄像头无法打开**
   - 检查摄像头是否被其他程序占用
   - 尝试更改摄像头ID (VideoCapture参数)

2. **检测精度不高**
   - 确保光照条件良好
   - 调整摄像头焦距和角度
   - 使用焦距校准功能

3. **距离测量不准确**
   - 按 **C** 查看校准说明
   - 使用已知距离的标记进行校准
   - 调整焦距参数

4. **箭头键无响应**
   - 使用备用按键 **W/D**
   - 检查终端输出的按键值进行调试

## 开发信息

- **开发语言**：Python
- **主要依赖**：OpenCV, NumPy
- **AprilTag字典**：DICT_APRILTAG_36h11
- **支持平台**：Windows, macOS, Linux

## 贡献

欢迎提交Issue和Pull Request来改进这个项目。

## 许可证

本项目采用MIT许可证。详见LICENSE文件。