FROM python:3.11.9-slim

# 设置工作目录
WORKDIR /app

# 复制项目文件
COPY . .

# 安装依赖
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# 启动服务
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "9235"]
