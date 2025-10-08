#!/bin/bash
# 系统状态检查脚本

set -e  # 遇到错误立即退出

echo "🔍 智投AI股票智能分析系统状态检查"

# 检查Docker是否安装
echo "🐳 检查Docker..."
if command -v docker &> /dev/null
then
    DOCKER_VERSION=$(docker --version)
    echo "✅ Docker已安装: $DOCKER_VERSION"
else
    echo "❌ Docker未安装"
    exit 1
fi

# 检查Docker Compose是否安装
echo "🚢 检查Docker Compose..."
if command -v docker-compose &> /dev/null
then
    DOCKER_COMPOSE_VERSION=$(docker-compose --version)
    echo "✅ Docker Compose已安装: $DOCKER_COMPOSE_VERSION"
else
    echo "❌ Docker Compose未安装"
    exit 1
fi

# 检查项目文件结构
echo "📁 检查项目结构..."
if [ -d "./gushi_backend" ] && [ -d "./gushi_frontend" ]; then
    echo "✅ 项目结构完整"
else
    echo "❌ 项目结构不完整"
    exit 1
fi

# 检查配置文件
echo "⚙️  检查配置文件..."
if [ -f "./.env" ]; then
    echo "✅ .env配置文件存在"
    
    # 检查必要配置项
    source ./.env
    if [ -n "$VOLC_API_KEY" ] && [ "$VOLC_API_KEY" != "your-volc-api-key-here" ]; then
        echo "✅ 火山引擎API密钥已配置"
    else
        echo "⚠️  火山引擎API密钥未配置"
    fi
    
    if [ -n "$QWEN_API_KEY" ] && [ "$QWEN_API_KEY" != "your-qwen-api-key-here" ]; then
        echo "✅ 通义千问API密钥已配置"
    else
        echo "⚠️  通义千问API密钥未配置"
    fi
else
    echo "❌ .env配置文件不存在"
fi

# 检查Docker服务状态
echo "サービ  检查Docker服务状态..."
if docker-compose ps | grep -q "Up"; then
    echo "✅ Docker服务正在运行"
    echo "📊 服务状态:"
    docker-compose ps
else
    echo "⚠️  Docker服务未运行"
    echo "💡 提示: 运行 ./start.sh 启动服务"
fi

# 检查端口占用
echo "🔌 检查端口占用..."
PORTS=(5000 3000 5432 6379)
for PORT in "${PORTS[@]}"; do
    if nc -z localhost $PORT; then
        echo "✅ 端口 $PORT 已被占用"
    else
        echo "⚠️  端口 $PORT 未被占用"
    fi
done

# 检查网络连接
echo "🌐 检查网络连接..."
API_ENDPOINTS=(
    "https://dashscope.aliyuncs.com"
    "https://ark.cn-beijing.volces.com"
    "https://api.akshare.com"
)

for ENDPOINT in "${API_ENDPOINTS[@]}"; do
    if curl -s --connect-timeout 5 $ENDPOINT > /dev/null; then
        echo "✅ 能够连接到 $ENDPOINT"
    else
        echo "❌ 无法连接到 $ENDPOINT"
    fi
done

# 检查磁盘空间
echo "💾 检查磁盘空间..."
DISK_USAGE=$(df -h . | awk 'NR==2 {print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -lt 80 ]; then
    echo "✅ 磁盘空间充足 ($DISK_USAGE%)"
else
    echo "⚠️  磁盘空间不足 ($DISK_USAGE%)"
fi

# 检查内存使用
echo "🧠 检查内存使用..."
MEMORY_USAGE=$(free | awk 'NR==2{printf "%.1f", $3*100/$2 }')
if (( $(echo "$MEMORY_USAGE < 80" | bc -l) )); then
    echo "✅ 内存使用正常 ($MEMORY_USAGE%)"
else
    echo "⚠️  内存使用过高 ($MEMORY_USAGE%)"
fi

# 检查CPU使用
echo "💻 检查CPU使用..."
CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | sed 's/%us,//')
if (( $(echo "$CPU_USAGE < 80" | bc -l) )); then
    echo "✅ CPU使用正常 ($CPU_USAGE%)"
else
    echo "⚠️  CPU使用过高 ($CPU_USAGE%)"
fi

# 检查日志文件
echo "📝 检查日志文件..."
if [ -d "./logs" ]; then
    LOG_COUNT=$(find ./logs -name "*.log" | wc -l)
    echo "✅ 日志目录存在，共 $LOG_COUNT 个日志文件"
else
    echo "⚠️  日志目录不存在"
fi

# 显示系统信息
echo "🖥️  系统信息:"
echo "  操作系统: $(uname -s)"
echo "  系统版本: $(uname -r)"
echo "  系统架构: $(uname -m)"
echo "  当前时间: $(date)"

echo "🎉 系统状态检查完成!"

# 提供建议
echo
echo "💡 系统维护建议:"
echo "  1. 定期备份数据: 运行 ./backup.sh"
echo "  2. 更新依赖包: 在gushi_backend和gushi_frontend目录分别运行 'pip install -r requirements.txt' 和 'npm install'"
echo "  3. 清理日志文件: 定期清理过期日志以节省磁盘空间"
echo "  4. 监控系统资源: 定期检查CPU、内存和磁盘使用情况"
echo "  5. 更新AI模型: 关注AI服务提供商的模型更新"

# 询问是否需要详细信息
echo
read -p "是否显示详细系统信息? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo "📋 详细系统信息:"
    echo "  Docker信息:"
    docker info | head -10
    echo
    echo "  Docker Compose信息:"
    docker-compose version
    echo
    echo "  Python版本:"
    python --version
    echo
    echo "  Node.js版本:"
    node --version
    echo
    echo "  npm版本:"
    npm --version
fi