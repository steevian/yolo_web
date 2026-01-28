import os

# 硬编码你的 weights 路径
weights_path = r"D:\cyd\Desktop\yolo_web\yolo_cropDisease_detection_flask\weights"

# 逐一验证关键信息
print("=== 路径测试 ===")
print(f"1. 权重目录路径: {weights_path}")
print(f"2. 目录是否存在: {os.path.exists(weights_path)}")

# 列出目录下所有文件
if os.path.exists(weights_path):
    files = [f for f in os.listdir(weights_path) if os.path.isfile(os.path.join(weights_path, f))]
    print(f"3. 目录下的文件列表: {files}")
    print(f"4. 文件数量: {len(files)}")
else:
    print("⚠️  目录不存在！")

# 验证模型文件是否存在（替换成你的模型文件名）
model_file = "strawberry_best.pt"  # 改成你实际的模型文件名
model_full_path = os.path.join(weights_path, model_file)
print(f"5. 模型文件 {model_file} 是否存在: {os.path.exists(model_full_path)}")