import cv2
import numpy as np
import time

def trackSign_CV():
    # ------ 1. 标签ID与交通标志类别映射 ------
    id_label_map = {
        0: "NO ENTRY",
        1: "DEAD END",
        2: "TURN RIGHT",
        3: "TURN LEFT",
        4: "FORWARD",
        5: "STOP"
    }
    # 距离估算用的假定实际标签宽(cm)，针对8-10cm标记优化
    TAG_WIDTH_CM = 9.0  # 8-10cm标记的平均尺寸
    focal_length = 1000  # 动态可调节的焦距值（改为小写变量名便于修改）
    FOCAL_STEP = 10     # 每次调整的焦距步长

    # ------ 2. 摄像头初始化 ------
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1080)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    # ------ 3. ArUco/AprilTag 参数设置 ------
    # 获取预定义的AprilTag 36h11字典，包含36个不同ID的标记，具有11位汉明距离的错误检测能力
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_APRILTAG_36h11)
    # 创建ArUco检测器参数对象，包含检测算法的所有可调节参数（阈值、轮廓检测等）
    parameters = cv2.aruco.DetectorParameters()
    
    # 针对8-10cm标记优化的检测参数
    parameters.adaptiveThreshWinSizeMin = 3         # 自适应阈值最小窗口
    parameters.adaptiveThreshWinSizeMax = 23        # 自适应阈值最大窗口
    parameters.adaptiveThreshWinSizeStep = 10       # 阈值窗口步长
    parameters.adaptiveThreshConstant = 7           # 阈值常数
    parameters.minMarkerPerimeterRate = 0.02        # 最小标记周长率（8cm标记需要更小值）
    parameters.maxMarkerPerimeterRate = 4.0         # 最大标记周长率
    parameters.polygonalApproxAccuracyRate = 0.05   # 多边形近似精度
    parameters.minCornerDistanceRate = 0.05         # 角点间最小距离
    parameters.minDistanceToBorder = 3              # 标记到边界最小距离
    parameters.cornerRefinementWinSize = 5          # 角点精化窗口大小
    parameters.cornerRefinementMaxIterations = 30   # 角点精化最大迭代次数
    
    # 设置角点精化方法为亚像素级精度，提高角点定位精度，对距离测量准确性很重要
    parameters.cornerRefinementMethod = cv2.aruco.CORNER_REFINE_SUBPIX

    last_time = time.time()
    stop_start_time = None  # 用于3秒停车逻辑

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Camera error")
            break

        # 图像预处理，提高8-10cm标记的检测精度
        gray_original = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # 轻微高斯模糊减少噪声（保持边缘清晰）
        gray_blurred = cv2.GaussianBlur(gray_original, (3, 3), 0)
        
        # 自适应直方图均衡化增强对比度
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        gray_enhanced = clahe.apply(gray_blurred)
        
        # 使用处理后的图像进行检测
        gray = gray_enhanced
        
        # AprilTag检测
        corners, ids, _ = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
        
        # 创建自适应阈值图像用于可视化检测过程
        adaptive_thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 7)
        
        # 创建处理步骤的显示图像，尺寸与主窗口一致
        # 获取主窗口尺寸
        main_height, main_width = frame.shape[:2]
        
        # 计算每个子图的尺寸（2x2布局）
        sub_width = main_width // 2
        sub_height = main_height // 2
        
        # 调整各个处理步骤图像的尺寸
        step1 = cv2.resize(gray_original, (sub_width, sub_height))     # 原始灰度图
        step2 = cv2.resize(gray_blurred, (sub_width, sub_height))      # 高斯模糊后
        step3 = cv2.resize(gray_enhanced, (sub_width, sub_height))     # 对比度增强后
        step4 = cv2.resize(adaptive_thresh, (sub_width, sub_height))   # 自适应阈值后
        
        # 在处理步骤图像上添加标题（字体大小根据窗口尺寸调整）
        font_scale = max(0.8, min(2.0, main_width / 800))  # 根据窗口宽度动态调整字体大小
        thickness = max(1, int(font_scale))
        
        cv2.putText(step1, "1. Original Gray", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), thickness)
        cv2.putText(step2, "2. Gaussian Blur", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), thickness)
        cv2.putText(step3, "3. CLAHE Enhanced", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), thickness)
        cv2.putText(step4, "4. Adaptive Threshold", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 0), thickness)
        
        # 创建上下两行显示，与主窗口尺寸一致
        top_row = np.hstack([step1, step2])
        bottom_row = np.hstack([step3, step4])
        processing_steps = np.vstack([top_row, bottom_row])

        action_display = "None"
        distance_display = "—"
        if ids is not None:
            for i, corner in enumerate(corners):
                tag_id = int(ids[i][0])
                
                # 计算标记尺寸进行过滤
                c = corner[0]
                side1 = np.linalg.norm(c[0] - c[1])
                side2 = np.linalg.norm(c[1] - c[2])
                px_size = (side1 + side2) / 2
                
                # 估算距离以判断标记是否在合理范围内
                if px_size > 0:
                    estimated_distance = (TAG_WIDTH_CM * focal_length) / px_size
                    
                    # 过滤：只处理距离在10-200cm之间的标记（8-10cm标记的合理检测范围）
                    if 10 <= estimated_distance <= 200:
                        action = id_label_map.get(tag_id, "UNKNOWN")

                        # 绘制边框、ID和动作
                        cv2.aruco.drawDetectedMarkers(frame, [corner], ids[i])

                        center = np.mean(c, axis=0).astype(int)
                        cv2.putText(frame, f"ID:{tag_id}", (center[0] - 30, center[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (30,255,30), 2)
                        cv2.putText(frame, f"{action}", (center[0] - 60, center[1] + 28), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 220, 220), 3)
                        action_display = action

                        # 距离显示
                        distance_display = f"{estimated_distance:.1f}cm"
                    else:
                        # 绘制被过滤的检测（灰色）
                        center = np.mean(c, axis=0).astype(int)
                        cv2.putText(frame, f"ID:{tag_id} (FILTERED)", (center[0] - 50, center[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (128,128,128), 1)

                # -- 停车动作3秒逻辑示例 --
                if action == "STOP":
                    if stop_start_time is None:
                        stop_start_time = time.time()
                    stop_elapsed = time.time() - stop_start_time
                    cv2.putText(frame, f"STOP: {stop_elapsed:.1f}s", (center[0] - 40, center[1] + 55), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                    if stop_elapsed < 3.0:
                        action_display = "STOP (WAITING...)"
                else:
                    stop_start_time = None
        else:
            stop_start_time = None

        # ------ 4. 显示FPS ------
        now = time.time()
        fps = 1.0 / (now - last_time)
        last_time = now
        cv2.putText(frame, f"FPS: {fps:.1f}", (12,36), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,0,0),2)
        # 距离和动作文字渲染
        cv2.putText(frame, f"Action: {action_display}", (13, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,120,255),2)
        cv2.putText(frame, f"Distance: {distance_display}", (13, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,200,200),2)
        
        # 添加检测状态信息
        detected_count = len(ids) if ids is not None else 0
        cv2.putText(frame, f"Detected: {detected_count} tags", (13, 145), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,0), 2)
        # 突出显示当前焦距值（带背景）
        focal_text = f"Focal Length: {focal_length}"
        (text_width, text_height), baseline = cv2.getTextSize(focal_text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
        cv2.rectangle(frame, (10, 160), (10 + text_width + 6, 160 + text_height + baseline + 6), (0, 0, 0), -1)
        cv2.putText(frame, focal_text, (13, 180), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2)
        cv2.putText(frame, "ESC: Exit | S: Save | UP/DOWN or W/D: Focal", (13, frame.shape[0] - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200,200,200), 1)
        cv2.putText(frame, "R: Reset focal | C: Calibration mode", (13, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200,200,200), 1)

        # 显示主检测窗口
        cv2.imshow("AprilTag 36h11 Detection (trackSign_CV)", frame)
        
        # 显示图像处理步骤窗口
        cv2.imshow("Image Processing Steps", processing_steps)
        
        # 按键控制
        key = cv2.waitKey(1) & 0xFF
        
        # 调试：显示按键值（可以看到实际的键值）
        if key != 255:  # 255表示没有按键
            print(f"Key pressed: {key}")
        
        if key == 27:  # ESC键退出
            break
        elif key == ord('s'):  # 按's'键保存当前处理步骤图像
            cv2.imwrite('processing_steps.jpg', processing_steps)
            print("Processing steps image saved as 'processing_steps.jpg'")
        # 多种箭头键值适配（不同系统可能不同）
        elif key in [82, 0, 65]:  # 上箭头键的多种可能值
            focal_length += FOCAL_STEP
            print(f"Focal length increased to: {focal_length}")
            # 在窗口上显示调整提示
            cv2.putText(frame, f"FOCAL LENGTH: {focal_length} (+{FOCAL_STEP})", (frame.shape[1]//2 - 150, 50), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 3)
            cv2.imshow("AprilTag 36h11 Detection (trackSign_CV)", frame)
            cv2.waitKey(500)  # 显示0.5秒
        elif key in [84, 1, 66]:  # 下箭头键的多种可能值
            focal_length = max(100, focal_length - FOCAL_STEP)  # 最小值限制为100
            print(f"Focal length decreased to: {focal_length}")
            # 在窗口上显示调整提示
            cv2.putText(frame, f"FOCAL LENGTH: {focal_length} (-{FOCAL_STEP})", (frame.shape[1]//2 - 150, 50), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 100, 255), 3)
            cv2.imshow("AprilTag 36h11 Detection (trackSign_CV)", frame)
            cv2.waitKey(500)  # 显示0.5秒
        # 添加备用按键：W/S键
        elif key == ord('w') or key == ord('W'):  # W键增加焦距
            focal_length += FOCAL_STEP
            print(f"Focal length increased to: {focal_length} (W key)")
            cv2.putText(frame, f"FOCAL LENGTH: {focal_length} (+{FOCAL_STEP})", (frame.shape[1]//2 - 150, 50), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 3)
            cv2.imshow("AprilTag 36h11 Detection (trackSign_CV)", frame)
            cv2.waitKey(500)
        elif key == ord('d') or key == ord('D'):  # D键减少焦距
            focal_length = max(100, focal_length - FOCAL_STEP)
            print(f"Focal length decreased to: {focal_length} (D key)")
            cv2.putText(frame, f"FOCAL LENGTH: {focal_length} (-{FOCAL_STEP})", (frame.shape[1]//2 - 150, 50), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 100, 255), 3)
            cv2.imshow("AprilTag 36h11 Detection (trackSign_CV)", frame)
            cv2.waitKey(500)
        elif key == ord('r') or key == ord('R'):  # 重置焦距为默认值
            focal_length = 1000
            print(f"Focal length reset to: {focal_length}")
            # 在窗口上显示重置提示
            cv2.putText(frame, f"FOCAL LENGTH RESET: {focal_length}", (frame.shape[1]//2 - 180, 50), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 0), 3)
            cv2.imshow("AprilTag 36h11 Detection (trackSign_CV)", frame)
            cv2.waitKey(800)  # 显示0.8秒
        elif key == ord('c') or key == ord('C'):  # 校准模式说明
            print("\n=== 焦距校准说明 ===")
            print("1. 将AprilTag放在已知距离处（如30cm）")
            print("2. 观察显示的距离值")
            print("3. 如果显示距离小于实际距离，按 '↑' 增加焦距")
            print("4. 如果显示距离大于实际距离，按 '↓' 减少焦距")
            print("5. 重复调整直到显示距离接近实际距离")
            print("6. 按 'R' 可重置焦距为1000")
            print("====================")

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    trackSign_CV()
