# -*- coding: utf-8 -*-
# @Time : 2024-12-26 12:10
# @Author : 林枫
# @File : predictImg.py
import json
import time
import torch  # 新增：导入torch，用于控制精度
from ultralytics import YOLO


class ImagePredictor:
    def __init__(self, weights_path, img_path, kind, save_path="./runs/result.jpg", conf=0.5):
        """
        初始化ImagePredictor类
        :param weights_path: 权重文件路径
        :param img_path: 输入图像路径
        :param save_path: 结果保存路径
        :param conf: 置信度阈值
        """
        # 核心修改1：加载模型时强制使用CPU + 单精度(float32)
        self.model = YOLO(weights_path)
        self.model.to(device='cpu', dtype=torch.float32)  # 强制CPU运行，单精度浮点
        
        self.conf = conf
        self.img_path = img_path
        self.save_path = save_path
        self.kind = {
            'rice': ['Brown_Spot（褐斑病）', 'Rice_Blast（稻瘟病）', 'Bacterial_Blight（细菌性叶枯病）'],
            'corn': ['blight（疫病）', 'common_rust（普通锈病）', 'gray_spot（灰斑病）', 'health（健康）'],
            'strawberry': ['Angular Leafspot（角斑病）', ' Anthracnose Fruit Rot（炭疽果腐病）', 'Blossom Blight（花枯病）', 'Gray Mold（灰霉病）', 'Leaf Spot（叶斑病）', 'Powdery Mildew Fruit（白粉病果）', 'Powdery Mildew Leaf（白粉病叶）'],
            'tomato': ['Early Blight（早疫病）', 'Healthy（健康）', 'Late Blight（晚疫病）', 'Leaf Miner（潜叶病）', 'Leaf Mold（叶霉病）', 'Mosaic Virus（花叶病毒）', 'Septoria（壳针孢属）', 'Spider Mites（蜘蛛螨）', 'Yellow Leaf Curl Virus（黄化卷叶病毒	）']
        }
        self.labels = self.kind[kind]

    def predict(self):
        """
        预测图像并保存结果
        """
        start_time = time.time()  # 开始计时

        # 核心修改2：关闭half=True（CPU不支持），强制device=cpu
        results = self.model(
            source=self.img_path, 
            conf=self.conf, 
            half=False,  # 关键：关闭半精度，CPU仅支持全精度
            save_conf=True,
            device='cpu'  # 明确指定CPU
        )

        end_time = time.time()  # 结束计时
        elapsed_time = end_time - start_time  # 计算用时

        # 核心修改3：返回数值型的耗时/置信度，适配后端BigDecimal接收
        all_results = {
            'labels': [],  # 存储所有标签
            'confidences': [],  # 存储数值型置信度（如0.95），而非字符串
            'allTime': elapsed_time  # 返回浮点数（秒），而非带单位的字符串
        }

        try:
            # 检查是否有检测结果
            if len(results) == 0:
                print("未检测到目标，请换一张图片。")
                all_results = {
                    'labels': '预测失败',
                    'confidences': 0.0,  # 数值型默认值
                    'allTime': elapsed_time
                }
                return all_results

            for result in results:
                # 提取置信度和标签
                confidences = result.boxes.conf if hasattr(result.boxes, 'conf') else []
                labels = result.boxes.cls if hasattr(result.boxes, 'cls') else []

                # 检查 confidences 和 labels 是否为空
                if confidences.numel() == 0 or labels.numel() == 0:
                    print("未检测到目标，请换一张图片。")
                    all_results = {
                        'labels': '预测失败',
                        'confidences': 0.0,  # 数值型默认值
                        'allTime': elapsed_time
                    }
                    return all_results

                # 获取标签名称和对应置信度（转为数值型）
                label_names = [self.labels[int(cls)] for cls in labels]
                # 核心修改4：置信度转为浮点数（如tensor(0.95) → 0.95）
                conf_values = [float(conf) for conf in confidences]
                
                predictions = list(zip(label_names, conf_values))

                # 将每个结果保存到字典中
                for label, conf in predictions:
                    all_results['labels'].append(label)
                    all_results['confidences'].append(conf)  # 存储数值，而非百分比字符串

                result.save(filename=self.save_path)  # 保存结果

            return all_results  # 返回包含标签和置信度的字典
        except Exception as e:
            # 如果预测过程中发生异常，打印错误信息并返回空结果
            print(f"预测过程中发生异常: {e}")
            all_results = {
                'labels': '预测失败',
                'confidences': 0.0,  # 数值型默认值
                'allTime': elapsed_time
            }
            return all_results


if __name__ == '__main__':
    # 初始化预测器
    predictor = ImagePredictor("../weights/rice_best.pt", "../rice_test.png", 'rice', save_path="../runs/result.jpg", conf=0.5)

    # 执行预测
    result = predictor.predict()
    labels_str = json.dumps(result['labels'], ensure_ascii=False)  # 保留中文
    confidences_str = json.dumps(result['confidences'], ensure_ascii=False)
    print("识别标签:", labels_str)
    print("置信度（数值）:", confidences_str)
    print("耗时（秒）:", result['allTime'])