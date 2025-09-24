# 机器人学与计算机视觉课程实验 | Autonomous Mobile Robotics Course Lab

**中文** | [English](#english-version)

## 课程概述 | Course Overview

本课程实验项目专注于机器人视觉系统的设计与实现，结合YOLO目标检测、OpenCV计算机视觉技术和LIMO小车平台，为学生提供完整的机器人视觉应用开发体验。通过AprilTag交通标志识别系统的开发，学生将掌握现代机器人视觉系统的核心技术。

This course lab project focuses on the design and implementation of robotic vision systems, combining YOLO object detection, OpenCV computer vision technology, and the LIMO robot platform to provide students with a complete robotic vision application development experience.

## 学习目标 | Learning Objectives

### 理论知识 | Theoretical Knowledge
- 🎯 **计算机视觉基础**：图像处理、特征提取、目标检测原理
- 🧠 **深度学习应用**：YOLO目标检测算法的理论与实践
- 📐 **几何视觉**：相机标定、距离测量、坐标变换
- 🤖 **机器人感知**：传感器融合、实时决策系统

### 实践技能 | Practical Skills
- 💻 **OpenCV编程**：图像处理、特征检测、相机操作
- 🔍 **YOLO模型部署**：模型训练、优化、实时推理
- 🚗 **LIMO小车控制**：硬件接口、运动控制、传感器集成
- 🏷️ **AprilTag系统**：标记检测、姿态估计、距离测量

## 实验环境要求 | Environment Requirements

### 硬件要求 | Hardware Requirements

#### LIMO小车平台 | LIMO Robot Platform
- **LIMO四轮差分机器人** 或 **LIMO Pro**
- **英特尔RealSense D435/D455深度相机** 或 **普通USB摄像头**
- **Jetson Nano/Xavier NX** 或 **树莓派4B**（推荐4GB+内存）
- **8GB+微SD卡**（用于系统存储）
- **充电器和数据线**

#### 实验辅助设备 | Lab Auxiliary Equipment
- **AprilTag标记卡片**（8-10cm，ID: 0-5）
- **测量工具**（尺子、量角器）
- **实验场地**（至少3m×3m的平坦区域）
- **良好照明环境**

### 软件环境 | Software Environment

#### 基础系统要求 | Basic System Requirements
```bash
# 支持的操作系统 | Supported Operating Systems
- Ubuntu 18.04/20.04/22.04 LTS
- Raspberry Pi OS (Bullseye)
- Jetson Nano Developer Kit SD Card Image

# Python版本要求 | Python Version Requirements
- Python 3.7+ (推荐 Python 3.8+)
```

#### 核心依赖库 | Core Dependencies
```python
# 计算机视觉库 | Computer Vision Libraries
opencv-python>=4.7.0          # OpenCV主库
opencv-contrib-python>=4.7.0   # OpenCV扩展库（包含ArUco模块）

# 数值计算库 | Numerical Computing Libraries
numpy>=1.23.0                  # 数值计算基础
matplotlib>=3.5.0              # 数据可视化

# 图像处理库 | Image Processing Libraries
imutils>=0.5.4                 # OpenCV工具集
Pillow>=9.0.0                  # 图像处理

# YOLO相关依赖 | YOLO Related Dependencies
ultralytics>=8.0.0            # YOLOv8官方库
torch>=1.12.0                 # PyTorch深度学习框架
torchvision>=0.13.0           # PyTorch视觉库

# 机器人控制库 | Robot Control Libraries  
rclpy                          # ROS2 Python客户端（适用于ROS2环境）
geometry_msgs                  # ROS几何消息
sensor_msgs                    # ROS传感器消息
```

## 技术栈详解 | Technology Stack Details

### 1. YOLO目标检测 | YOLO Object Detection

#### YOLO算法原理 | YOLO Algorithm Principles
```python
# YOLOv8模型集成示例 | YOLOv8 Model Integration Example
from ultralytics import YOLO

class TrafficSignYOLO:
    def __init__(self, model_path="yolov8n.pt"):
        self.model = YOLO(model_path)
        self.traffic_signs = {
            0: "NO_ENTRY", 1: "DEAD_END", 2: "TURN_RIGHT",
            3: "TURN_LEFT", 4: "FORWARD", 5: "STOP"
        }
    
    def detect_signs(self, frame):
        """使用YOLO检测交通标志"""
        results = self.model(frame)
        detections = []
        
        for r in results:
            boxes = r.boxes
            if boxes is not None:
                for box in boxes:
                    # 提取边界框和置信度
                    xyxy = box.xyxy[0].cpu().numpy()
                    conf = box.conf[0].cpu().numpy()
                    cls = int(box.cls[0].cpu().numpy())
                    
                    if conf > 0.5:  # 置信度阈值
                        detections.append({
                            'bbox': xyxy,
                            'confidence': conf,
                            'class': self.traffic_signs.get(cls, 'UNKNOWN')
                        })
        
        return detections
```

#### YOLO模型训练 | YOLO Model Training
```bash
# 数据集准备 | Dataset Preparation
mkdir -p datasets/traffic_signs/{train,val}/{images,labels}

# 模型训练命令 | Model Training Commands
yolo train data=traffic_signs.yaml model=yolov8n.pt epochs=100 imgsz=640

# 模型验证 | Model Validation
yolo val model=runs/detect/train/weights/best.pt data=traffic_signs.yaml
```

### 2. OpenCV计算机视觉 | OpenCV Computer Vision

#### 图像预处理管道 | Image Preprocessing Pipeline
```python
def enhanced_preprocessing(frame):
    """增强的图像预处理流程"""
    # 1. 颜色空间转换
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # 2. 高斯模糊降噪
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    
    # 3. CLAHE对比度增强
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(blurred)
    
    # 4. 自适应阈值二值化
    binary = cv2.adaptiveThreshold(
        enhanced, 255, cv2.ADAPTIVE_THRESH_MEAN_C, 
        cv2.THRESH_BINARY, 11, 7
    )
    
    return {
        'original': gray,
        'blurred': blurred, 
        'enhanced': enhanced,
        'binary': binary
    }
```

#### AprilTag检测优化 | AprilTag Detection Optimization
```python
def setup_apriltag_detector():
    """配置AprilTag检测器参数"""
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_APRILTAG_36h11)
    parameters = cv2.aruco.DetectorParameters()
    
    # 针对8-10cm标记的优化参数
    parameters.adaptiveThreshWinSizeMin = 3
    parameters.adaptiveThreshWinSizeMax = 23
    parameters.minMarkerPerimeterRate = 0.02  # 小尺寸标记
    parameters.cornerRefinementMethod = cv2.aruco.CORNER_REFINE_SUBPIX
    
    return aruco_dict, parameters
```

### 3. LIMO小车集成 | LIMO Robot Integration

#### ROS2通信架构 | ROS2 Communication Architecture
```python
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

class LimoVisionController(Node):
    def __init__(self):
        super().__init__('limo_vision_controller')
        
        # 发布器：运动控制
        self.cmd_vel_publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        
        # 订阅器：相机图像
        self.image_subscription = self.create_subscription(
            Image, '/camera/image_raw', self.image_callback, 10
        )
        
        self.bridge = CvBridge()
        self.yolo_detector = TrafficSignYOLO()
    
    def image_callback(self, msg):
        """处理相机图像并执行决策"""
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
            
            # YOLO检测
            detections = self.yolo_detector.detect_signs(cv_image)
            
            # 根据检测结果控制小车
            self.execute_traffic_sign_action(detections)
            
        except Exception as e:
            self.get_logger().error(f'Image processing error: {e}')
    
    def execute_traffic_sign_action(self, detections):
        """根据交通标志执行对应动作"""
        cmd = Twist()
        
        for detection in detections:
            sign_type = detection['class']
            
            if sign_type == 'STOP':
                # 停车3秒
                cmd.linear.x = 0.0
                cmd.angular.z = 0.0
                self.get_logger().info('STOP sign detected - stopping for 3 seconds')
                
            elif sign_type == 'TURN_LEFT':
                # 左转
                cmd.linear.x = 0.2
                cmd.angular.z = 0.5
                
            elif sign_type == 'TURN_RIGHT':
                # 右转
                cmd.linear.x = 0.2
                cmd.angular.z = -0.5
                
            elif sign_type == 'FORWARD':
                # 直行
                cmd.linear.x = 0.3
                cmd.angular.z = 0.0
        
        self.cmd_vel_publisher.publish(cmd)
```

## 快速开始 | Quick Start

### 1. 环境配置 | Environment Setup

```bash
# 克隆项目 | Clone Repository
git clone https://github.com/your-username/robotics_limo_assignment.git
cd robotics_limo_assignment

# 创建虚拟环境 | Create Virtual Environment
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate  # Windows

# 安装依赖 | Install Dependencies
pip install -r requirements.txt

# 验证安装 | Verify Installation
python -c "import cv2, numpy, ultralytics; print('Environment setup successful!')"
```

### 2. LIMO小车配置 | LIMO Robot Configuration

```bash
# 连接LIMO小车 | Connect to LIMO Robot
# 方法1：WiFi连接（推荐）
ssh agilex@192.168.1.100  # 默认IP地址

# 方法2：串口连接
sudo minicom -D /dev/ttyUSB0 -b 115200

# 检查LIMO状态 | Check LIMO Status
rostopic list  # ROS1环境
ros2 topic list  # ROS2环境

# 启动相机节点 | Start Camera Node
ros2 run usb_cam usb_cam_node_exe --ros-args -p video_device:="/dev/video0"
```

### 3. 运行实验 | Run Experiments

#### 实验1：AprilTag检测 | Experiment 1: AprilTag Detection
```bash
cd assignment1
python CPSC_5207EL_A1_Gx_CV.py

# 操作说明 | Operation Instructions
# ESC: 退出程序 | Exit program
# S: 保存处理步骤图像 | Save processing steps
# W/D: 调整焦距 | Adjust focal length
# R: 重置焦距 | Reset focal length
# C: 校准模式说明 | Calibration instructions
```

#### 实验2：YOLO+LIMO集成 | Experiment 2: YOLO+LIMO Integration
```bash
# 启动ROS2环境 | Start ROS2 Environment
source /opt/ros/foxy/setup.bash  # 或其他ROS2版本

# 运行LIMO控制节点 | Run LIMO Control Node
ros2 run limo_vision_pkg limo_vision_controller

# 在新终端中监控话题 | Monitor topics in new terminal
ros2 topic echo /cmd_vel
```

## 实验任务 | Lab Assignments

### Assignment 1: AprilTag交通标志识别 | AprilTag Traffic Sign Recognition
- **目标**：实现基于AprilTag的交通标志检测与距离测量
- **要求**：
  - 支持6种交通标志类型识别
  - 实时距离测量（精度±2cm）
  - 图像处理流程可视化
  - 动态焦距校准功能

### Assignment 2: YOLO目标检测系统 | YOLO Object Detection System
- **目标**：开发基于YOLOv8的交通标志检测系统
- **要求**：
  - 训练自定义YOLO模型
  - 实现实时检测（>10 FPS）
  - 检测精度>90%
  - 支持多目标同时检测

### Assignment 3: LIMO小车自主导航 | LIMO Autonomous Navigation
- **目标**：集成视觉系统与LIMO小车，实现自主导航
- **要求**：
  - 基于交通标志的决策系统
  - 安全停车机制
  - 路径规划与避障
  - 实时状态监控

## 评分标准 | Grading Criteria

| 评估项目 | 权重 | 评分标准 |
|---------|------|----------|
| **代码实现** | 40% | 代码质量、功能完整性、算法正确性 |
| **系统性能** | 25% | 检测精度、实时性、稳定性 |
| **创新设计** | 20% | 算法优化、功能扩展、用户体验 |
| **实验报告** | 15% | 技术文档、结果分析、问题解决 |

## 常见问题解决 | Troubleshooting

### 环境问题 | Environment Issues

#### Q1: OpenCV安装失败
```bash
# 解决方案1：使用conda安装
conda install -c conda-forge opencv

# 解决方案2：从源码编译
git clone https://github.com/opencv/opencv.git
cd opencv && mkdir build && cd build
cmake -D CMAKE_BUILD_TYPE=Release -D CMAKE_INSTALL_PREFIX=/usr/local ..
make -j4 && sudo make install
```

#### Q2: LIMO小车连接问题
```bash
# 检查网络连接
ping 192.168.1.100

# 检查串口权限
sudo usermod -a -G dialout $USER
sudo chmod 666 /dev/ttyUSB0

# 重启网络服务
sudo systemctl restart NetworkManager
```

### 性能优化 | Performance Optimization

#### 提高检测精度 | Improve Detection Accuracy
- 确保充足光照条件
- 调整相机焦距和角度
- 使用高质量AprilTag标记
- 优化图像预处理参数

#### 提升运行速度 | Improve Running Speed
- 降低图像分辨率（如640×480）
- 使用GPU加速（CUDA）
- 优化检测参数
- 减少不必要的图像处理步骤

## 扩展学习 | Extended Learning

### 进阶项目 | Advanced Projects
- **多机器人协作**：多LIMO小车协同导航
- **SLAM建图**：同步定位与地图构建
- **语义分割**：场景理解与路径规划
- **强化学习**：智能决策与路径优化

### 相关课程 | Related Courses
- 机器学习与深度学习
- 机器人操作系统（ROS）
- 计算机视觉算法
- 自动驾驶技术

## 参考资源 | References

### 官方文档 | Official Documentation
- [OpenCV Documentation](https://docs.opencv.org/)
- [YOLO Official Repository](https://github.com/ultralytics/ultralytics)
- [ROS2 Documentation](https://docs.ros.org/en/foxy/)
- [LIMO User Manual](https://docs.agilex.ai/)

### 学术论文 | Academic Papers
- AprilTag: A robust and flexible visual fiducial system
- YOLOv8: Real-time object detection with improved accuracy
- ROS: an open-source Robot Operating System

### 在线教程 | Online Tutorials
- [OpenCV Python Tutorials](https://opencv-python-tutroals.readthedocs.io/)
- [Deep Learning for Computer Vision](https://www.coursera.org/learn/convolutional-neural-networks)
- [ROS2 Tutorials](https://docs.ros.org/en/foxy/Tutorials.html)

---

## English Version

### Course Overview
This robotics and computer vision lab course combines YOLO object detection, OpenCV computer vision techniques, and the LIMO robot platform to provide comprehensive hands-on experience in robotic vision systems development.

### Learning Objectives
- Master computer vision fundamentals and deep learning applications
- Develop proficiency in OpenCV programming and YOLO model deployment
- Gain experience with robotic hardware integration and control
- Build real-world autonomous navigation systems

### Technology Stack
- **YOLO**: State-of-the-art object detection for traffic sign recognition
- **OpenCV**: Comprehensive computer vision library for image processing
- **LIMO Robot**: Versatile robot platform for autonomous navigation
- **ROS2**: Robot Operating System for communication and control

### Quick Start Guide
1. **Environment Setup**: Install Python 3.7+, OpenCV 4.7+, and required dependencies
2. **Hardware Configuration**: Connect LIMO robot and camera system
3. **Run Experiments**: Execute AprilTag detection and YOLO integration demos
4. **Advanced Projects**: Develop autonomous navigation and multi-robot systems

For detailed English documentation, please refer to the assignment-specific README files in each subdirectory.

---

## 许可证 | License

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 贡献 | Contributing

欢迎提交 Issue 和 Pull Request 来改进这个项目。

Welcome to submit Issues and Pull Requests to improve this project.

## 联系方式 | Contact

如有问题，请联系课程助教或访问项目 GitHub 页面。

For questions, please contact the course TAs or visit the project GitHub page.