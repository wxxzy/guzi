# 使用官方Python基础镜像
FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY gushi_backend/requirements.txt .

# 安装系统依赖
RUN apt-get update && apt-get install -y \\
    gcc \\
    g++ \\
    && rm -rf /var/lib/apt/lists/*

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY gushi_backend/ .

# 创建上传目录
RUN mkdir -p uploads

# 暴露端口
EXPOSE 5000

# 设置环境变量
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production

# 运行应用
CMD [\"gunicorn\", \"--bind\", \"0.0.0.0:5000\", \"--workers\", \"4\", \"--timeout\", \"120\", \"app:app\"]