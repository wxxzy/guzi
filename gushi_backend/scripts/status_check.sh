#!/bin/bash
# 智投AI股票智能分析系统状态检查脚本

set -e  # 遇到错误立即退出

echo "🔍 开始检查智投AI股票智能分析系统状态..."

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

echo "✅ Docker环境检查通过"

# 检查服务状态
echo
echo "📊 检查服务状态..."
docker-compose ps

# 检查各组件状态
echo
echo "🔧 检查各组件状态..."

# 检查后端服务
echo "🌐 检查后端服务..."
if docker-compose ps | grep backend | grep -q "Up"; then
    echo "✅ 后端服务运行正常"
    BACKEND_STATUS="正常"
else
    echo "❌ 后端服务未运行"
    BACKEND_STATUS="异常"
fi

# 检查数据库服务
echo "🗄️  检查数据库服务..."
if docker-compose ps | grep db | grep -q "Up"; then
    echo "✅ 数据库服务运行正常"
    DB_STATUS="正常"
else
    echo "❌ 数据库服务未运行"
    DB_STATUS="异常"
fi

# 检查Redis服务
echo "キャッシング 检查Redis服务..."
if docker-compose ps | grep redis | grep -q "Up"; then
    echo "✅ Redis服务运行正常"
    REDIS_STATUS="正常"
else
    echo "❌ Redis服务未运行"
    REDIS_STATUS="异常"
fi

# 检查前端服务
echo "🖥️  检查前端服务..."
if docker-compose ps | grep frontend | grep -q "Up"; then
    echo "✅ 前端服务运行正常"
    FRONTEND_STATUS="正常"
else
    echo "❌ 前端服务未运行"
    FRONTEND_STATUS="异常"
fi

# 检查Nginx服务
echo "🔁 检查Nginx服务..."
if docker-compose ps | grep nginx | grep -q "Up"; then
    echo "✅ Nginx服务运行正常"
    NGINX_STATUS="正常"
else
    echo "❌ Nginx服务未运行"
    NGINX_STATUS="异常"
fi

# 检查网络连接
echo
echo "📡 检查网络连接..."

# 检查后端API
echo "🔗 检查后端API连接..."
if curl -s -f http://localhost:5000/health > /dev/null; then
    echo "✅ 后端API连接正常"
    API_STATUS="正常"
else
    echo "❌ 后端API连接异常"
    API_STATUS="异常"
fi

# 检查前端页面
echo "🌐 检查前端页面连接..."
if curl -s -f http://localhost:3000 > /dev/null; then
    echo "✅ 前端页面连接正常"
    FRONTEND_ACCESS_STATUS="正常"
else
    echo "❌ 前端页面连接异常"
    FRONTEND_ACCESS_STATUS="异常"
fi

# 检查数据库连接
echo "🔌 检查数据库连接..."
if docker-compose exec db pg_isready -U gushi_user > /dev/null 2>&1; then
    echo "✅ 数据库连接正常"
    DB_CONNECTION_STATUS="正常"
else
    echo "❌ 数据库连接异常"
    DB_CONNECTION_STATUS="异常"
fi

# 检查Redis连接
echo "⚡ 检查Redis连接..."
if docker-compose exec redis redis-cli ping > /dev/null 2>&1; then
    echo "✅ Redis连接正常"
    REDIS_CONNECTION_STATUS="正常"
else
    echo "❌ Redis连接异常"
    REDIS_CONNECTION_STATUS="异常"
fi

# 检查AI服务连接
echo
echo "🤖 检查AI服务连接..."

# 检查通义千问服务
echo "🧠 检查通义千问服务..."
if [ -n "$QWEN_API_KEY" ] && [ "$QWEN_API_KEY" != "your-qwen-api-key-here" ]; then
    echo "✅ 通义千问API密钥已配置"
    QWEN_STATUS="已配置"
else
    echo "⚠️  通义千问API密钥未配置"
    QWEN_STATUS="未配置"
fi

# 检查火山引擎服务
echo "🌋 检查火山引擎服务..."
if [ -n "$VOLC_API_KEY" ] && [ "$VOLC_API_KEY" != "your-volc-api-key-here" ]; then
    echo "✅ 火山引擎API密钥已配置"
    VOLC_STATUS="已配置"
else
    echo "⚠️  火山引擎API密钥未配置"
    VOLC_STATUS="未配置"
fi

# 检查OpenAI服务
echo "🔗 检查OpenAI服务..."
if [ -n "$OPENAI_API_KEY" ] && [ "$OPENAI_API_KEY" != "your-openai-api-key-here" ]; then
    echo "✅ OpenAI API密钥已配置"
    OPENAI_STATUS="已配置"
else
    echo "⚠️  OpenAI API密钥未配置"
    OPENAI_STATUS="未配置"
fi

# 生成状态报告
echo
echo "📋 系统状态报告"
echo "================"
echo "组件状态:"
echo "  后端服务: $BACKEND_STATUS"
echo "  数据库服务: $DB_STATUS"
echo "  Redis服务: $REDIS_STATUS"
echo "  前端服务: $FRONTEND_STATUS"
echo "  Nginx服务: $NGINX_STATUS"
echo
echo "连接状态:"
echo "  后端API: $API_STATUS"
echo "  前端页面: $FRONTEND_ACCESS_STATUS"
echo "  数据库连接: $DB_CONNECTION_STATUS"
echo "  Redis连接: $REDIS_CONNECTION_STATUS"
echo
echo "AI服务状态:"
echo "  通义千问: $QWEN_STATUS"
echo "  火山引擎: $VOLC_STATUS"
echo "  OpenAI: $OPENAI_STATUS"
echo

# 总体评估
echo "🎯 总体评估:"
if [ "$BACKEND_STATUS" = "正常" ] && [ "$DB_STATUS" = "正常" ] && [ "$API_STATUS" = "正常" ]; then
    echo "✅ 系统核心组件运行正常"
else
    echo "⚠️  系统存在异常组件，请检查日志"
fi

# 提供操作建议
echo
echo "💡 操作建议:"
if [ "$BACKEND_STATUS" != "正常" ] || [ "$DB_STATUS" != "正常" ]; then
    echo "  - 使用 './start.sh' 启动服务"
elif [ "$API_STATUS" != "正常" ]; then
    echo "  - 检查后端服务日志: docker-compose logs backend"
elif [ "$DB_CONNECTION_STATUS" != "正常" ]; then
    echo "  - 检查数据库服务日志: docker-compose logs db"
elif [ "$REDIS_CONNECTION_STATUS" != "正常" ]; then
    echo "  - 检查Redis服务日志: docker-compose logs redis"
fi

if [ "$QWEN_STATUS" = "未配置" ] || [ "$VOLC_STATUS" = "未配置" ]; then
    echo "  - 请在 .env 文件中配置AI服务API密钥"
fi

echo
echo "📈 详细服务信息:"
docker-compose ps

echo
echo "🎉 状态检查完成!"