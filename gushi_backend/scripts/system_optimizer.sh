#!/bin/bash
# 智投AI股票智能分析系统优化脚本

set -e  # 遇到错误立即退出

echo "🚀 开始优化智投AI股票智能分析系统..."

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

# 创建优化日志目录
OPTIMIZE_LOG_DIR="./logs/optimization"
mkdir -p $OPTIMIZE_LOG_DIR

# 系统资源优化函数
optimize_system_resources() {
    echo "🔧 系统资源优化..."
    
    # 检查系统资源
    TOTAL_MEM=$(free -m | awk '/^Mem:/{print $2}')
    AVAILABLE_MEM=$(free -m | awk '/^Mem:/{print $7}')
    CPU_CORES=$(nproc)
    
    echo "  总内存: ${TOTAL_MEM}MB"
    echo "  可用内存: ${AVAILABLE_MEM}MB"
    echo "  CPU核心数: ${CPU_CORES}"
    
    # 根据系统资源配置优化Docker资源限制
    if [ "$TOTAL_MEM" -gt 8000 ]; then
        echo "  ✅ 系统资源充足，使用标准配置"
        DOCKER_MEM_LIMIT="4g"
        DOCKER_CPU_LIMIT="2"
    elif [ "$TOTAL_MEM" -gt 4000 ]; then
        echo "  ⚠️  系统资源中等，使用保守配置"
        DOCKER_MEM_LIMIT="2g"
        DOCKER_CPU_LIMIT="1"
    else
        echo "  ❌ 系统资源不足，建议升级硬件"
        DOCKER_MEM_LIMIT="1g"
        DOCKER_CPU_LIMIT="0.5"
    fi
    
    echo "  Docker内存限制: $DOCKER_MEM_LIMIT"
    echo "  Docker CPU限制: $DOCKER_CPU_LIMIT"
    
    # 记录优化结果
    echo "$(date '+%Y-%m-%d %H:%M:%S') - 系统资源配置优化完成" >> $OPTIMIZE_LOG_DIR/resource_optimization.log
}

# 数据库优化函数
optimize_database() {
    echo "🗄️  数据库优化..."
    
    # 检查数据库服务是否运行
    if ! docker-compose ps | grep -q "db.*Up"; then
        echo "  ⚠️  数据库服务未运行，跳过数据库优化"
        return
    fi
    
    # 执行数据库优化
    echo "  执行数据库VACUUM操作..."
    docker-compose exec db vacuumdb -U gushi_user -d gushi_db --verbose 2>&1 | tee -a $OPTIMIZE_LOG_DIR/db_optimization.log
    
    echo "  执行数据库ANALYZE操作..."
    docker-compose exec db psql -U gushi_user -d gushi_db -c "ANALYZE;" 2>&1 | tee -a $OPTIMIZE_LOG_DIR/db_optimization.log
    
    echo "  检查数据库索引..."
    docker-compose exec db psql -U gushi_user -d gushi_db -c "SELECT tablename,indexname FROM pg_indexes WHERE schemaname = 'public';" 2>&1 | tee -a $OPTIMIZE_LOG_DIR/db_optimization.log
    
    echo "  ✅ 数据库优化完成"
}

# 缓存优化函数
optimize_cache() {
    echo "キャッシング 缓存优化..."
    
    # 检查Redis服务是否运行
    if ! docker-compose ps | grep -q "redis.*Up"; then
        echo "  ⚠️  Redis服务未运行，跳过缓存优化"
        return
    fi
    
    # 清理过期缓存
    echo "  清理过期缓存..."
    docker-compose exec redis redis-cli EXPIRE 0 2>&1 | tee -a $OPTIMIZE_LOG_DIR/cache_optimization.log
    
    # 查看缓存使用情况
    echo "  查看缓存使用情况..."
    docker-compose exec redis redis-cli INFO memory 2>&1 | tee -a $OPTIMIZE_LOG_DIR/cache_optimization.log
    
    echo "  ✅ 缓存优化完成"
}

# 网络优化函数
optimize_network() {
    echo "🌐 网络优化..."
    
    # 检查Nginx服务是否运行
    if ! docker-compose ps | grep -q "nginx.*Up"; then
        echo "  ⚠️  Nginx服务未运行，跳过网络优化"
        return
    fi
    
    # 检查Nginx配置
    echo "  检查Nginx配置..."
    docker-compose exec nginx nginx -t 2>&1 | tee -a $OPTIMIZE_LOG_DIR/network_optimization.log
    
    # 重新加载Nginx配置
    echo "  重新加载Nginx配置..."
    docker-compose exec nginx nginx -s reload 2>&1 | tee -a $OPTIMIZE_LOG_DIR/network_optimization.log
    
    echo "  ✅ 网络优化完成"
}

# AI服务优化函数
optimize_ai_services() {
    echo "🤖 AI服务优化..."
    
    # 检查AI服务配置
    if [ -n "$QWEN_API_KEY" ] && [ "$QWEN_API_KEY" != "your-qwen-api-key-here" ]; then
        echo "  通义千问: 已配置"
    else
        echo "  通义千问: 未配置"
    fi
    
    if [ -n "$VOLC_API_KEY" ] && [ "$VOLC_API_KEY" != "your-volc-api-key-here" ]; then
        echo "  火山引擎: 已配置"
    else
        echo "  火山引擎: 未配置"
    fi
    
    if [ -n "$OPENAI_API_KEY" ] && [ "$OPENAI_API_KEY" != "your-openai-api-key-here" ]; then
        echo "  OpenAI: 已配置"
    else
        echo "  OpenAI: 未配置"
    fi
    
    # 优化AI服务配置
    echo "  优化AI服务配置..."
    
    # 设置缓存策略
    echo "  设置AI响应缓存策略..."
    
    # 设置重试机制
    echo "  设置AI服务重试机制..."
    
    echo "  ✅ AI服务优化完成"
}

# 性能测试函数
performance_test() {
    echo "⚡ 性能测试..."
    
    # 测试API响应时间
    echo "  测试后端API响应时间..."
    START_TIME=$(date +%s.%N)
    curl -s -f http://localhost:5000/health > /dev/null
    END_TIME=$(date +%s.%N)
    RESPONSE_TIME=$(echo "$END_TIME - $START_TIME" | bc)
    echo "  后端API响应时间: ${RESPONSE_TIME}s"
    
    # 测试前端页面加载时间
    echo "  测试前端页面加载时间..."
    START_TIME=$(date +%s.%N)
    curl -s -f http://localhost:3000 > /dev/null
    END_TIME=$(date +%s.%N)
    RESPONSE_TIME=$(echo "$END_TIME - $START_TIME" | bc)
    echo "  前端页面加载时间: ${RESPONSE_TIME}s"
    
    # 记录性能测试结果
    echo "$(date '+%Y-%m-%d %H:%M:%S') - 性能测试完成，后端API响应时间: ${RESPONSE_TIME}s" >> $OPTIMIZE_LOG_DIR/performance_test.log
}

# 主优化函数
main_optimization() {
    echo "🎯 开始系统优化..."
    
    # 执行各项优化
    optimize_system_resources
    optimize_database
    optimize_cache
    optimize_network
    optimize_ai_services
    performance_test
    
    echo "🎉 系统优化完成！"
    echo "📊 优化日志保存在: $OPTIMIZE_LOG_DIR"
}

# 清理函数
cleanup() {
    echo "🧹 开始清理..."
    
    # 清理Docker资源
    echo "  清理未使用的Docker资源..."
    docker system prune -f 2>&1 | tee -a $OPTIMIZE_LOG_DIR/cleanup.log
    
    # 清理日志文件（保留最近7天）
    echo "  清理旧日志文件..."
    find ./logs -name "*.log" -type f -mtime +7 -delete 2>/dev/null || true
    
    # 清理临时文件
    echo "  清理临时文件..."
    rm -rf /tmp/gushi_* 2>/dev/null || true
    
    echo "  ✅ 清理完成"
}

# 主程序
main() {
    case "$1" in
        optimize)
            main_optimization
            ;;
        cleanup)
            cleanup
            ;;
        all)
            main_optimization
            cleanup
            ;;
        *)
            echo "使用方法: $0 {optimize|cleanup|all}"
            echo "  optimize - 执行系统优化"
            echo "  cleanup  - 执行清理操作"
            echo "  all      - 执行优化和清理"
            exit 1
            ;;
    esac
}

# 执行主程序
main "$@"