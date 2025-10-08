#!/bin/bash
# 查看日志脚本

set -e  # 遇到错误立即退出

SERVICE_NAME=${1:-all}

echo "查看股票智能分析系统日志..."
echo "服务: ${SERVICE_NAME}"

# 检查Docker是否安装
if ! command -v docker &> /dev/null
then
    echo "错误: Docker未安装"
    exit 1
fi

# 检查Docker Compose是否安装
if ! command -v docker-compose &> /dev/null
then
    echo "错误: Docker Compose未安装"
    exit 1
fi

# 查看指定服务的日志
case $SERVICE_NAME in
    "backend")
        docker-compose logs -f backend
        ;;
    "db")
        docker-compose logs -f db
        ;;
    "redis")
        docker-compose logs -f redis
        ;;
    "nginx")
        docker-compose logs -f nginx
        ;;
    "frontend")
        docker-compose logs -f frontend
        ;;
    *)
        echo "查看所有服务日志..."
        docker-compose logs -f
        ;;
esac