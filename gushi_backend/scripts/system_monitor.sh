#!/bin/bash
# 智投AI股票智能分析系统监控脚本

set -e  # 遇到错误立即退出

echo "📊 开始监控智投AI股票智能分析系统..."

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

# 创建监控日志目录
LOG_DIR="./logs/monitoring"
mkdir -p $LOG_DIR

# 监控函数
monitor_system() {
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    LOG_FILE="$LOG_DIR/system_monitor_$(date '+%Y%m%d').log"
    
    echo "[$TIMESTAMP] === 系统监控报告 ===" >> $LOG_FILE
    
    # 1. 系统资源监控
    echo "[$TIMESTAMP] 系统资源使用情况:" >> $LOG_FILE
    echo "  CPU使用率: $(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | awk -F'%' '{print $1}')%" >> $LOG_FILE
    echo "  内存使用率: $(free | grep Mem | awk '{printf("%.2f%%", $3/$2 * 100.0)}')" >> $LOG_FILE
    echo "  磁盘使用率: $(df -h / | awk 'NR==2{print $5}')" >> $LOG_FILE
    
    # 2. Docker容器监控
    echo "[$TIMESTAMP] Docker容器状态:" >> $LOG_FILE
    docker-compose ps >> $LOG_FILE
    
    # 3. 服务健康检查
    echo "[$TIMESTAMP] 服务健康检查:" >> $LOG_FILE
    
    # 检查后端API
    if curl -s -f http://localhost:5000/health > /dev/null; then
        echo "  后端API: 健康" >> $LOG_FILE
    else
        echo "  后端API: 异常" >> $LOG_FILE
    fi
    
    # 检查前端页面
    if curl -s -f http://localhost:3000 > /dev/null; then
        echo "  前端页面: 健康" >> $LOG_FILE
    else
        echo "  前端页面: 异常" >> $LOG_FILE
    fi
    
    # 检查数据库连接
    if docker-compose exec db pg_isready -U gushi_user > /dev/null 2>&1; then
        echo "  数据库连接: 健康" >> $LOG_FILE
    else
        echo "  数据库连接: 异常" >> $LOG_FILE
    fi
    
    # 检查Redis连接
    if docker-compose exec redis redis-cli ping > /dev/null 2>&1; then
        echo "  Redis连接: 健康" >> $LOG_FILE
    else
        echo "  Redis连接: 异常" >> $LOG_FILE
    fi
    
    # 4. AI服务状态检查
    echo "[$TIMESTAMP] AI服务状态:" >> $LOG_FILE
    
    # 检查环境变量
    if [ -n "$QWEN_API_KEY" ] && [ "$QWEN_API_KEY" != "your-qwen-api-key-here" ]; then
        echo "  通义千问: 已配置" >> $LOG_FILE
    else
        echo "  通义千问: 未配置" >> $LOG_FILE
    fi
    
    if [ -n "$VOLC_API_KEY" ] && [ "$VOLC_API_KEY" != "your-volc-api-key-here" ]; then
        echo "  火山引擎: 已配置" >> $LOG_FILE
    else
        echo "  火山引擎: 未配置" >> $LOG_FILE
    fi
    
    if [ -n "$OPENAI_API_KEY" ] && [ "$OPENAI_API_KEY" != "your-openai-api-key-here" ]; then
        echo "  OpenAI: 已配置" >> $LOG_FILE
    else
        echo "  OpenAI: 未配置" >> $LOG_FILE
    fi
    
    # 5. 性能指标
    echo "[$TIMESTAMP] 性能指标:" >> $LOG_FILE
    echo "  系统负载: $(uptime | awk -F'load average:' '{print $2}')" >> $LOG_FILE
    echo "  进程数: $(ps aux | wc -l)" >> $LOG_FILE
    
    echo "[$TIMESTAMP] === 监控报告结束 ===" >> $LOG_FILE
    echo "" >> $LOG_FILE
    
    # 输出到控制台
    echo "[$TIMESTAMP] 监控完成，详情请查看 $LOG_FILE"
}

# 实时监控函数
realtime_monitor() {
    echo "🔄 开始实时监控 (按 Ctrl+C 停止)..."
    
    while true; do
        TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
        echo "[$TIMESTAMP] 系统状态快照:"
        
        # 显示简要状态
        echo "  CPU: $(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | awk -F'%' '{print $1}')%"
        echo "  内存: $(free | grep Mem | awk '{printf("%.1f%%", $3/$2 * 100.0)}')"
        echo "  磁盘: $(df -h / | awk 'NR==2{print $5}')"
        
        # 显示容器状态
        UP_CONTAINERS=$(docker-compose ps | grep "Up" | wc -l)
        TOTAL_CONTAINERS=$(docker-compose ps | grep -v "Name" | grep -v "----------" | wc -l)
        echo "  容器: $UP_CONTAINERS/$TOTAL_CONTAINERS 运行中"
        
        # 检查关键服务
        if curl -s -f http://localhost:5000/health > /dev/null; then
            echo "  后端API: ✅ 健康"
        else
            echo "  后端API: ❌ 异常"
        fi
        
        if curl -s -f http://localhost:3000 > /dev/null; then
            echo "  前端页面: ✅ 健康"
        else
            echo "  前端页面: ❌ 异常"
        fi
        
        echo "---"
        sleep 30
    done
}

# 警报检查函数
check_alerts() {
    ALERT_LOG="$LOG_DIR/alerts_$(date '+%Y%m%d').log"
    
    # 检查CPU使用率
    CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | awk -F'%' '{print $1}' | cut -d'.' -f1)
    if [ "$CPU_USAGE" -gt 80 ]; then
        echo "$(date '+%Y-%m-%d %H:%M:%S') [ALERT] CPU使用率过高: ${CPU_USAGE}%" >> $ALERT_LOG
    fi
    
    # 检查内存使用率
    MEMORY_USAGE=$(free | grep Mem | awk '{printf("%.0f", $3/$2 * 100.0)}')
    if [ "$MEMORY_USAGE" -gt 80 ]; then
        echo "$(date '+%Y-%m-%d %H:%M:%S') [ALERT] 内存使用率过高: ${MEMORY_USAGE}%" >> $ALERT_LOG
    fi
    
    # 检查磁盘使用率
    DISK_USAGE=$(df -h / | awk 'NR==2{print $5}' | sed 's/%//')
    if [ "$DISK_USAGE" -gt 80 ]; then
        echo "$(date '+%Y-%m-%d %H:%M:%S') [ALERT] 磁盘使用率过高: ${DISK_USAGE}%" >> $ALERT_LOG
    fi
    
    # 检查服务状态
    if ! curl -s -f http://localhost:5000/health > /dev/null; then
        echo "$(date '+%Y-%m-%d %H:%M:%S') [ALERT] 后端API服务异常" >> $ALERT_LOG
    fi
    
    if ! curl -s -f http://localhost:3000 > /dev/null; then
        echo "$(date '+%Y-%m-%d %H:%M:%S') [ALERT] 前端页面服务异常" >> $ALERT_LOG
    fi
}

# 主程序
main() {
    case "$1" in
        once)
            echo "🔍 执行一次性监控..."
            monitor_system
            check_alerts
            ;;
        realtime)
            echo "🔄 执行实时监控..."
            realtime_monitor
            ;;
        *)
            echo "使用方法: $0 {once|realtime}"
            echo "  once     - 执行一次性监控"
            echo "  realtime - 执行实时监控"
            exit 1
            ;;
    esac
}

# 执行主程序
main "$@"