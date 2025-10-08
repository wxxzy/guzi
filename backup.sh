#!/bin/bash
# 备份智投AI股票智能分析系统数据

set -e  # 遇到错误立即退出

echo "💾 开始备份智投AI股票智能分析系统数据..."

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

# 创建备份目录
BACKUP_DIR="./backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_NAME="gushi_backup_$TIMESTAMP"

mkdir -p $BACKUP_DIR
echo "📁 备份目录: $BACKUP_DIR"
echo "📅 备份时间戳: $TIMESTAMP"

# 备份数据库
echo "🗄️  开始备份数据库..."
docker-compose exec db pg_dump -U gushi_user -d gushi_db > "$BACKUP_DIR/${BACKUP_NAME}_database.sql"

# 备份配置文件
echo "⚙️  开始备份配置文件..."
cp .env "$BACKUP_DIR/${BACKUP_NAME}_config.env" 2>/dev/null || echo "⚠️  未找到.env配置文件"

# 备份日志文件
echo "📝 开始备份日志文件..."
if [ -d "./logs" ]; then
    tar -czf "$BACKUP_DIR/${BACKUP_NAME}_logs.tar.gz" ./logs 2>/dev/null || echo "⚠️  日志备份失败"
else
    echo "⚠️  未找到日志目录"
fi

# 备份应用数据
echo "📊 开始备份应用数据..."
if [ -d "./data" ]; then
    tar -czf "$BACKUP_DIR/${BACKUP_NAME}_data.tar.gz" ./data 2>/dev/null || echo "⚠️  应用数据备份失败"
else
    echo "⚠️  未找到应用数据目录"
fi

# 创建备份信息文件
cat > "$BACKUP_DIR/${BACKUP_NAME}_info.txt" << EOF
智投AI股票智能分析系统备份信息
================================

备份时间: $(date)
备份名称: $BACKUP_NAME
备份文件:
  - 数据库: ${BACKUP_NAME}_database.sql
  - 配置文件: ${BACKUP_NAME}_config.env
  - 日志文件: ${BACKUP_NAME}_logs.tar.gz
  - 应用数据: ${BACKUP_NAME}_data.tar.gz

系统信息:
  - 操作系统: $(uname -s)
  - 系统版本: $(uname -r)
  - 备份工具版本: 1.0.0
EOF

# 显示备份结果
echo "✅ 备份完成!"
echo "📦 备份文件列表:"
ls -lh $BACKUP_DIR/${BACKUP_NAME}*

# 清理旧备份（保留最近7天）
echo "🧹 清理旧备份（保留最近7天）..."
find $BACKUP_DIR -name "gushi_backup_*" -type f -mtime +7 -delete 2>/dev/null || true

echo "🎉 备份任务完成!"
echo "📂 备份文件保存在: $BACKUP_DIR"
echo "📎 备份名称: $BACKUP_NAME"