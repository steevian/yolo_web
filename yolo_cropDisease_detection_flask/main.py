# -*- coding: utf-8 -*-
# @Time : 2024-12-2024/12/26 23:21
# @Author : 林枫
# @File : main.py

import json
import os
import subprocess
import cv2
import requests
import torch  # 新增：导入torch控制精度
from flask import Flask, Response, request
from ultralytics import YOLO
from predict import predictImg
from flask_socketio import SocketIO, emit


# Flask 应用设置
class VideoProcessingApp:
    def __init__(self, host='0.0.0.0', port=5000):
        """初始化 Flask 应用并设置路由"""
        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")  # 初始化 SocketIO
        self.host = host
        self.port = port
        self.setup_routes()
        self.data = {}  # 存储接收参数
        self.paths = {
            'download': './runs/video/download.mp4',
            'output': './runs/video/output.mp4',
            'camera_output': "./runs/video/camera_output.avi",
            'video_output': "./runs/video/camera_output.avi"
        }
        self.recording = False  # 标志位，判断是否正在录制视频
        # 新增：模型根目录（统一管理）
        self.weights_root = r"D:\cyd\Desktop\yolo_web\yolo_cropDisease_detection_flask\weights"
        # 新增：系统字体路径（统一管理，避免重复定义）
        self.system_font_path = "C:/Windows/Fonts/msyh.ttc"  # 微软雅黑

    def setup_routes(self):
        """设置所有路由"""
        self.app.add_url_rule('/file_names', 'file_names', self.file_names, methods=['GET'])
        # 修复：添加前端需要的 /predict 接口（映射到原 predictImg 方法）
        self.app.add_url_rule('/predict', 'predict', self.predictImg, methods=['POST'])
        # 保留原有 /predictImg 接口（兼容）
        self.app.add_url_rule('/predictImg', 'predictImg', self.predictImg, methods=['POST'])
        self.app.add_url_rule('/predictVideo', 'predictVideo', self.predictVideo)
        self.app.add_url_rule('/predictCamera', 'predictCamera', self.predictCamera)
        self.app.add_url_rule('/stopCamera', 'stopCamera', self.stopCamera, methods=['GET'])

        # 添加 WebSocket 事件
        @self.socketio.on('connect')
        def handle_connect():
            print("WebSocket connected!")
            emit('message', {'data': 'Connected to WebSocket server!'})

        @self.socketio.on('disconnect')
        def handle_disconnect():
            print("WebSocket disconnected!")

    def run(self):
        """启动 Flask 应用"""
        self.socketio.run(self.app, host=self.host, port=self.port, allow_unsafe_werkzeug=True)

    def file_names(self):
        """模型列表接口 - 强制返回模型列表"""
        print("=== 我是新的 file_names 方法，正在执行！===")  # 新增这行
        try:
            weight_items = [
                {'value': 'corn_best.pt', 'label': 'corn_best.pt'},
                {'value': 'rice_best.pt', 'label': 'rice_best.pt'},
                {'value': 'strawberry_best.pt', 'label': 'strawberry_best.pt'},
                {'value': 'tomato_best.pt', 'label': 'tomato_best.pt'}
            ]
            return json.dumps({'weight_items': weight_items}, ensure_ascii=False)
        except Exception as e:
            print(f"获取模型列表失败: {e}")
            return json.dumps({'weight_items': []}, ensure_ascii=False)

    def predictImg(self):
        """图片预测接口 - 核心修复：定义model_path + 兼容参数 + CPU精度强制"""
        try:
            # 修复：兼容表单提交和 JSON 提交
            if request.is_json:
                data = request.get_json()
            else:
                data = request.form.to_dict()
            
            print("接收的预测参数:", data)
            
            # 参数校验（非必填参数不强制校验，避免前端传参不全报错）
            required_params = ['weight', 'inputImg']  # 仅保留核心必填参数
            for param in required_params:
                if param not in data or not data[param]:
                    return json.dumps({
                        "status": 400,
                        "message": f"缺少必要参数: {param}",
                        "label": "",
                        "confidence": 0.0,  # 返回数值而非字符串
                        "allTime": 0.0,      # 返回数值而非字符串
                        "outImg": ""
                    }, ensure_ascii=False)
            
            # 补充默认值，避免参数为空
            self.data.clear()
            self.data.update({
                "username": data.get('username', ''), 
                "weight": data['weight'],
                "conf": float(data.get('conf', 0.5)),  # 转为浮点数，设置默认值0.5
                "startTime": data.get('startTime', ''),
                "inputImg": data['inputImg'],
                "kind": data.get('kind', '')
            })
            
            # 核心修复1：定义model_path（拼接绝对路径）
            model_path = os.path.join(self.weights_root, self.data["weight"])
            print(f"模型路径: {model_path}")
            # 检查模型文件是否存在
            if not os.path.exists(model_path):
                return json.dumps({
                    "status": 404,
                    "message": f"模型文件不存在: {model_path}",
                    "label": "",
                    "confidence": 0.0,
                    "allTime": 0.0,
                    "outImg": ""
                }, ensure_ascii=False)
            
            # 核心修复2：创建预测器（移除不兼容的device/precision参数，predictImg.py已内置CPU配置）
            predict = predictImg.ImagePredictor(
                weights_path=model_path,
                img_path=self.data["inputImg"], 
                save_path='./runs/result.jpg', 
                kind=self.data["kind"],
                conf=float(self.data["conf"])
            )
            
            # 核心修复3：强制模型使用CPU + float32（兜底，确保精度正确）
            predict.model.to(device='cpu', dtype=torch.float32)
            
            # 执行预测
            results = predict.predict()
            
            # 处理预测结果 - 关键修复：统一返回数值类型
            if results.get('labels') != '预测失败' and results.get('labels'):
                # 上传结果图片
                uploadedUrl = self.upload('./runs/result.jpg') or ""
                
                # 处理 confidence：数组取平均值/第一个值，转为浮点数
                confidences = results.get('confidences', [])
                confidence_val = 0.0
                if isinstance(confidences, list) and len(confidences) > 0:
                    # 取第一个置信度值，或计算平均值
                    confidence_val = float(confidences[0]) if confidences[0] else 0.0
                
                # 处理 allTime：转为浮点数
                all_time_val = float(results.get('allTime', 0.0)) if results.get('allTime') else 0.0
                
                # 处理 label：数组转字符串，方便后端存储
                labels = results.get('labels', [])
                label_str = ",".join(labels) if isinstance(labels, list) else str(labels)
                
                response_data = {
                    "status": 200,
                    "message": "预测成功",
                    "outImg": uploadedUrl,
                    "allTime": all_time_val,          # 数值类型
                    "confidence": confidence_val,    # 数值类型（非数组）
                    "label": label_str,              # 字符串类型（非数组）
                    # 保留原数组字段，兼容后续扩展
                    "confidences": results.get('confidences', []),
                    "labels": results.get('labels', [])
                }
            else:
                response_data = {
                    "status": 400,
                    "message": "该图片无法识别，请重新上传！",
                    "label": "",
                    "confidence": 0.0,  # 数值类型
                    "allTime": 0.0,      # 数值类型
                    "outImg": ""
                }
            
            # 清理临时文件
            path = self.data["inputImg"].split('/')[-1]
            if os.path.exists('./' + path):
                os.remove('./' + path)
            
            # 确保返回格式前端能解析
            return json.dumps(response_data, ensure_ascii=False)
            
        except Exception as e:
            print(f"图片预测失败: {e}")
            # 返回统一的错误格式 - 数值类型默认值
            return json.dumps({
                "status": 500,
                "message": f"预测出错: {str(e)}",
                "label": "",
                "confidence": 0.0,  # 数值类型
                "allTime": 0.0,      # 数值类型
                "outImg": ""
            }, ensure_ascii=False)

    def predictVideo(self):
        """视频流处理接口 - 新增：指定系统字体，避免字体下载"""
        self.data.clear()
        self.data.update({
            "username": request.args.get('username'), "weight": request.args.get('weight'),
            "conf": request.args.get('conf'), "startTime": request.args.get('startTime'),
            "inputVideo": request.args.get('inputVideo'),
            "kind": request.args.get('kind')
        })
        self.download(self.data["inputVideo"], self.paths['download'])
        cap = cv2.VideoCapture(self.paths['download'])
        if not cap.isOpened():
            raise ValueError("无法打开视频文件")
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        print(fps)

        # 视频写入器
        video_writer = cv2.VideoWriter(
            self.paths['video_output'],
            cv2.VideoWriter_fourcc(*'XVID'),
            fps,
            (640, 480)
        )
        
        # 使用硬编码的绝对路径加载模型
        model_path = os.path.join(self.weights_root, self.data["weight"])
        model = YOLO(model_path)
        # 新增：视频预测也强制CPU + float32
        model.to(device='cpu', dtype=torch.float32)

        def generate():
            try:
                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        break
                    frame = cv2.resize(frame, (640, 480))
                    # 核心修改：添加font参数，使用系统自带字体
                    results = model.predict(
                        source=frame, 
                        conf=float(self.data['conf']), 
                        show=False, 
                        half=False,
                        font=self.system_font_path  # 指定系统字体，避免下载
                    )
                    processed_frame = results[0].plot(font=self.system_font_path)  # 绘制时也指定字体
                    video_writer.write(processed_frame)
                    _, jpeg = cv2.imencode('.jpg', processed_frame)
                    yield b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n'
            finally:
                self.cleanup_resources(cap, video_writer)
                self.socketio.emit('message', {'data': '处理完成，正在保存！'})
                for progress in self.convert_avi_to_mp4(self.paths['video_output']):
                    self.socketio.emit('progress', {'data': progress})
                uploadedUrl = self.upload(self.paths['output'])
                self.data["outVideo"] = uploadedUrl
                self.save_data(json.dumps(self.data), 'http://localhost:9999/videoRecords')
                self.cleanup_files([self.paths['download'], self.paths['output'], self.paths['video_output']])

        return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

    def predictCamera(self):
        """摄像头视频流处理接口 - 新增：指定系统字体，避免字体下载"""
        self.data.clear()
        self.data.update({
            "username": request.args.get('username'), "weight": request.args.get('weight'),
            "kind": request.args.get('kind'),
            "conf": request.args.get('conf'), "startTime": request.args.get('startTime')
        })
        self.socketio.emit('message', {'data': '正在加载，请稍等！'})
        
        # 使用硬编码的绝对路径加载模型
        model_path = os.path.join(self.weights_root, self.data["weight"])
        model = YOLO(model_path)
        # 新增：摄像头预测也强制CPU + float32
        model.to(device='cpu', dtype=torch.float32)
        
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        video_writer = cv2.VideoWriter(self.paths['camera_output'], cv2.VideoWriter_fourcc(*'XVID'), 20, (640, 480))
        self.recording = True

        def generate():
            try:
                while self.recording:
                    ret, frame = cap.read()
                    if not ret:
                        break
                    # 核心修改：添加font参数，使用系统自带字体
                    results = model.predict(
                        source=frame, 
                        imgsz=640, 
                        conf=float(self.data['conf']), 
                        show=False, 
                        half=False,
                        font=self.system_font_path  # 指定系统字体，避免下载
                    )
                    processed_frame = results[0].plot(font=self.system_font_path)  # 绘制时也指定字体
                    if self.recording and video_writer:
                        video_writer.write(processed_frame)
                    _, jpeg = cv2.imencode('.jpg', processed_frame)
                    yield b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n'
            finally:
                self.cleanup_resources(cap, video_writer)
                self.socketio.emit('message', {'data': '处理完成，正在保存！'})
                for progress in self.convert_avi_to_mp4(self.paths['camera_output']):
                    self.socketio.emit('progress', {'data': progress})
                uploadedUrl = self.upload(self.paths['output'])
                self.data["outVideo"] = uploadedUrl
                print(self.data)
                self.save_data(json.dumps(self.data), 'http://localhost:9999/cameraRecords')
                self.cleanup_files([self.paths['download'], self.paths['output'], self.paths['camera_output']])

        return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

    def stopCamera(self):
        """停止摄像头预测"""
        self.recording = False
        return json.dumps({"status": 200, "message": "预测成功", "code": 0})

    def save_data(self, data, path):
        """将结果数据上传到服务器"""
        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.post(path, data=data, headers=headers)
            print("记录上传成功！" if response.status_code == 200 else f"记录上传失败，状态码: {response.status_code}")
        except requests.RequestException as e:
            print(f"上传记录时发生错误: {str(e)}")

    def convert_avi_to_mp4(self, temp_output):
        """使用 FFmpeg 将 AVI 格式转换为 MP4 格式，并显示转换进度。"""
        ffmpeg_command = f"ffmpeg -i {temp_output} -vcodec libx264 {self.paths['output']} -y"
        process = subprocess.Popen(ffmpeg_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   text=True)
        total_duration = self.get_video_duration(temp_output)

        for line in process.stderr:
            if "time=" in line:
                try:
                    time_str = line.split("time=")[1].split(" ")[0]
                    h, m, s = map(float, time_str.split(":"))
                    processed_time = h * 3600 + m * 60 + s
                    if total_duration > 0:
                        progress = (processed_time / total_duration) * 100
                        yield progress
                except Exception as e:
                    print(f"解析进度时发生错误: {e}")

        process.wait()
        yield 100

    def get_video_duration(self, path):
        """获取视频总时长（秒）"""
        try:
            cap = cv2.VideoCapture(path)
            if not cap.isOpened():
                return 0
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            cap.release()
            return total_frames / fps if fps > 0 else 0
        except Exception:
            return 0

    def get_file_names(self, directory):
        """获取指定文件夹中的所有文件名 - 备用方法（当前未使用）"""
        try:
            # 硬编码 weights 目录的绝对路径（Windows 路径用 r 前缀避免转义）
            abs_directory = self.weights_root
            
            # 打印调试信息（方便排查）
            print(f"\n=== 路径调试信息 ===")
            print(f"硬编码的模型目录路径: {abs_directory}")
            print(f"目录是否存在: {os.path.exists(abs_directory)}")
            
            # 确保目录存在
            if not os.path.exists(abs_directory):
                os.makedirs(abs_directory, exist_ok=True)
                print(f"已创建目录: {abs_directory}")
                return []
            
            # 获取目录下所有文件
            file_list = [file for file in os.listdir(abs_directory) if os.path.isfile(os.path.join(abs_directory, file))]
            print(f"读取到的模型文件列表: {file_list}")
            print(f"====================\n")
            
            return file_list
        except Exception as e:
            print(f"获取文件列表失败: {e}")
            return []

    def upload(self, out_path):
        """上传处理后的图片或视频文件到远程服务器 - 修复：增强错误处理"""
        upload_url = "http://localhost:9999/files/upload"
        try:
            if not os.path.exists(out_path):
                print(f"文件不存在: {out_path}")
                return ""
            
            with open(out_path, 'rb') as file:
                files = {'file': (os.path.basename(out_path), file)}
                response = requests.post(upload_url, files=files, timeout=30)
                if response.status_code == 200:
                    print("文件上传成功！")
                    return response.json().get('data', "")
                else:
                    print(f"文件上传失败，状态码: {response.status_code}")
                    return ""
        except Exception as e:
            print(f"上传文件时发生错误: {str(e)}")
            return ""

    def download(self, url, save_path):
        """下载文件并保存到指定路径"""
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        try:
            with requests.get(url, stream=True, timeout=30) as response:
                response.raise_for_status()
                with open(save_path, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            file.write(chunk)
            print(f"文件已成功下载并保存到 {save_path}")
        except requests.RequestException as e:
            print(f"下载失败: {e}")

    def cleanup_files(self, file_paths):
        """清理文件 - 修复：增强异常处理"""
        for path in file_paths:
            try:
                if os.path.exists(path):
                    os.remove(path)
                    print(f"已删除文件: {path}")
            except Exception as e:
                print(f"删除文件 {path} 失败: {e}")

    def cleanup_resources(self, cap, video_writer):
        """释放资源"""
        try:
            if cap and cap.isOpened():
                cap.release()
            if video_writer:
                video_writer.release()
            cv2.destroyAllWindows()
        except Exception as e:
            print(f"释放资源失败: {e}")


# 启动应用
if __name__ == '__main__':
    # 确保必要目录存在
    base_dir = r"D:\cyd\Desktop\yolo_web\yolo_cropDisease_detection_flask"
    for dir_name in ['runs', 'runs/video', 'runs/images']:
        dir_path = os.path.join(base_dir, dir_name)
        os.makedirs(dir_path, exist_ok=True)
    
    video_app = VideoProcessingApp()
    video_app.run()