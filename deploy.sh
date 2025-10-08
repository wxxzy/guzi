#!/bin/bash
# 部署脚本

set -e  # 遇到错误立即退出

echo "开始部署股票智能分析系统..."

# 检查Docker是否安装
if ! command -v docker &> /dev/null
then
    echo "错误: Docker未安装，请先安装Docker"
    exit 1
fi

# 检查Docker Compose是否安装
if ! command -v docker-compose &> /dev/null
then
    echo "错误: Docker Compose未安装，请先安装Docker Compose"
    exit 1
fi

# 检查.env文件是否存在
if [ ! -f ".env" ]; then
    echo "警告: .env文件不存在，请先创建.env文件并配置环境变量"
    echo "可以复制.env.example文件并修改:"
    echo "cp .env.example .env"
    echo "然后编辑.env文件填入实际值"
    exit 1
fi

# 构建Docker镜像
echo "正在构建Docker镜像..."
docker-compose build

# 启动服务
echo "正在启动服务..."
docker-compose up -d

# 等待服务启动
echo "等待服务启动..."
sleep 10

# 检查服务状态
echo "检查服务状态..."
if docker-compose ps | grep -q "Up"; then
    echo "服务已成功启动!"
    echo "后端API地址: http://localhost:5000"
    echo "前端地址: http://localhost:3000"
    echo "数据库地址: localhost:5432"
else
    echo "服务启动失败，请检查日志:"
    docker-compose logs
    exit 1
fi

echo "部署完成!"