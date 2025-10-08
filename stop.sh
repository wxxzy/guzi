#!/bin/bash
# 停止智投AI股票智能分析系统

set -e  # 遇到错误立即退出

echo "⏹️  停止智投AI股票智能分析系统..."

# 检查Docker是否安装
if ! command -v docker &> /dev/null
then
    echo "❌ 错误: 未安装Docker"
    exit 1
fi

# 检查Docker Compose是否安装
if ! command -v docker-compose &> /dev/null
then
    echo "❌ 错误: 未安装Docker Compose"
    exit 1
fi

# 停止并移除容器
echo "🛑 停止并移除容器..."
docker-compose down

echo "✅ 系统已成功停止!"

# 显示服务状态
echo "📊 当前服务状态:"
docker-compose ps

# 提供清理选项
echo
echo "🧹 清理选项:"
echo "  1) 清理未使用的Docker镜像"
echo "  2) 清理未使用的Docker卷"
echo "  3) 清理所有数据（包括数据库）"
echo "  4) 退出"
read -p "请选择操作 (1-4): " choice

case $choice in
    1)
        echo "🧹 清理未使用的Docker镜像..."
        docker image prune -f
        echo "✅ 清理完成"
        ;;
    2)
        echo "🧹 清理未使用的Docker卷..."
        docker volume prune -f
        echo "✅ 清理完成"
        ;;
    3)
        echo "⚠️  警告: 此操作将删除所有数据，包括数据库!"
        read -p "确定要继续吗? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]
        then
            echo "🗑️  删除所有数据..."
            docker volume rm $(docker volume ls -q) 2>/dev/null || true
            echo "✅ 所有数据已删除"
        else
            echo "❌ 操作已取消"
        fi
        ;;
    4)
        echo "👋 退出系统管理"
        exit 0
        ;;
    *)
        echo "❌ 无效选择"
        ;;
esac

echo "👋 系统管理结束"