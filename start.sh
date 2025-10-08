#!/bin/bash
# 启动智投AI股票智能分析系统

set -e  # 遇到错误立即退出

echo "🚀 启动智投AI股票智能分析系统..."

# 检查Docker是否安装
if ! command -v docker &> /dev/null
then
    echo "❌ 错误: 未安装Docker，请先安装Docker"
    exit 1
fi

# 检查Docker Compose是否安装
if ! command -v docker-compose &> /dev/null
then
    echo "❌ 错误: 未安装Docker Compose，请先安装Docker Compose"
    exit 1
fi

# 检查.env文件是否存在
if [ ! -f ".env" ]; then
    echo "⚠️  警告: .env文件不存在"
    echo "💡 提示: 请复制 .env.example 文件并命名为 .env，然后填写实际配置"
    read -p "是否继续使用默认配置启动? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]
    then
        echo "❌ 启动已取消"
        exit 1
    fi
fi

# 检查必要配置
if [ -f ".env" ]; then
    source .env
    
    # 检查必要配置项
    if [ -z "$VOLC_API_KEY" ] || [ "$VOLC_API_KEY" = "your-volc-api-key-here" ]; then
        echo "⚠️  警告: 未配置火山引擎API密钥"
        echo "💡 提示: 请在.env文件中设置VOLC_API_KEY以启用AI分析功能"
    fi
    
    if [ -z "$QWEN_API_KEY" ] || [ "$QWEN_API_KEY" = "your-qwen-api-key-here" ]; then
        echo "⚠️  警告: 未配置通义千问API密钥"
        echo "💡 提示: 请在.env文件中设置QWEN_API_KEY以启用AI分析功能"
    fi
fi

# 构建Docker镜像
echo "🔨 构建Docker镜像..."
docker-compose build

# 启动服务
echo "🚀 启动服务..."
docker-compose up -d

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 10

# 检查服务状态
echo "🔍 检查服务状态..."
if docker-compose ps | grep -q "Up"; then
    echo "✅ 服务已成功启动!"
    
    # 显示服务端口
    echo "🌐 服务访问地址:"
    echo "   后端API: http://localhost:5000"
    echo "   前端应用: http://localhost:3000"
    echo "   数据库: localhost:5432"
    echo "   Redis: localhost:6379"
    
    # 显示日志查看命令
    echo "📋 查看日志:"
    echo "   docker-compose logs -f"
    
    # 显示停止命令
    echo "⏹️  停止服务:"
    echo "   docker-compose down"
else
    echo "❌ 服务启动失败，请检查日志:"
    docker-compose logs
    exit 1
fi

echo "🎉 智投AI股票智能分析系统启动完成!"

# 提供交互式菜单
while true; do
    echo
    echo "🔧 系统管理菜单:"
    echo "  1) 查看日志"
    echo "  2) 停止服务"
    echo "  3) 重启服务"
    echo "  4) 退出"
    read -p "请选择操作 (1-4): " choice
    
    case $choice in
        1)
            echo "📝 查看日志 (按 Ctrl+C 退出)..."
            docker-compose logs -f
            ;;
        2)
            echo "⏹️  停止服务..."
            docker-compose down
            echo "✅ 服务已停止"
            exit 0
            ;;
        3)
            echo "🔄 重启服务..."
            docker-compose down
            sleep 3
            docker-compose up -d
            echo "✅ 服务已重启"
            ;;
        4)
            echo "👋 退出系统管理"
            exit 0
            ;;
        *)
            echo "❌ 无效选择，请重新输入"
            ;;
    esac
done