# -*- coding: utf-8 -*-
import torch
from ultralytics import YOLO

# 替换为你的模型路径（和main.py中一致）
MODEL_PATH = "./weights/corn_best.pt"  # 可改为 rice_best.pt/tomato_best.pt

def check_model_device_and_precision():
    """验证模型的设备和精度"""
    print("===== 模型精度/设备验证 =====")
    
    # 1. 加载模型并强制CPU + float32
    model = YOLO(MODEL_PATH)
    model.to(device='cpu', dtype=torch.float32)
    
    # 2. 检查模型设备
    print(f"✅ 模型当前设备: {model.device}")
    
    # 3. 检查模型参数精度
    first_param = next(model.parameters())
    dtype = first_param.dtype
    print(f"✅ 模型参数精度: {dtype}")
    
    # 4. 验证是否为CPU兼容格式
    if model.device.type == 'cpu' and dtype == torch.float32:
        print("\n🎉 验证通过！模型已使用 CPU + float32（单精度），兼容CPU运行")
    else:
        print("\n❌ 验证失败！模型配置不兼容CPU：")
        if model.device.type != 'cpu':
            print("   - 模型未运行在CPU上（当前：{}）".format(model.device.type))
        if dtype != torch.float32:
            print("   - 模型精度不是float32（当前：{}），CPU不支持该精度".format(dtype))
    
    # 5. 测试预测（模拟实际调用）
    print("\n===== 测试CPU预测 =====")
    try:
        # 用空图片路径测试（仅验证模型推理逻辑）
        results = model(
            source="./test.png",  # 随便填一个路径，仅测试推理初始化
            conf=0.5,
            half=False,  # 强制关闭半精度
            device='cpu'
        )
        print("✅ 预测初始化成功，CPU推理逻辑正常")
    except Exception as e:
        if "slow_conv2d_cpu not implemented for 'Half'" in str(e):
            print("❌ 错误：模型仍在使用半精度！请检查predictImg.py中half=True是否改为False")
        else:
            print(f"❌ 预测测试失败：{str(e)[:100]}")

if __name__ == "__main__":
    check_model_device_and_precision()