#!/bin/bash
# 恢复智投AI股票智能分析系统数据

set -e  # 遇到错误立即退出

echo "🔄 开始恢复智投AI股票智能分析系统数据..."

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

# 显示可用备份
echo "📂 可用备份文件:"
BACKUP_DIR="./backups"
if [ -d "$BACKUP_DIR" ]; then
    ls -1 $BACKUP_DIR/gushi_backup_*_info.txt 2>/dev/null | sed 's/_info.txt$//' | sed 's|.*/||' || echo "未找到备份文件"
else
    echo "未找到备份目录"
    exit 1
fi

# 选择备份文件
echo
read -p "请输入要恢复的备份名称 (例如: gushi_backup_20231007_103000): " BACKUP_NAME

if [ -z "$BACKUP_NAME" ]; then
    echo "❌ 错误: 未指定备份名称"
    exit 1
fi

# 检查备份文件是否存在
if [ ! -f "$BACKUP_DIR/${BACKUP_NAME}_info.txt" ]; then
    echo "❌ 错误: 备份文件不存在"
    exit 1
fi

echo "📄 备份信息:"
cat "$BACKUP_DIR/${BACKUP_NAME}_info.txt"

# 确认恢复操作
echo
echo "⚠️  警告: 此操作将覆盖当前数据!"
read -p "确定要继续恢复吗? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    echo "❌ 恢复操作已取消"
    exit 0
fi

# 停止服务
echo "🛑 停止当前服务..."
docker-compose down

# 恢复数据库
echo "🗄️  恢复数据库..."
if [ -f "$BACKUP_DIR/${BACKUP_NAME}_database.sql" ]; then
    # 启动数据库服务
    docker-compose up -d db
    
    # 等待数据库启动
    echo "⏳ 等待数据库启动..."
    sleep 10
    
    # 恢复数据库
    docker-compose exec -T db psql -U gushi_user -d gushi_db < "$BACKUP_DIR/${BACKUP_NAME}_database.sql"
    echo "✅ 数据库恢复完成"
else
    echo "⚠️  未找到数据库备份文件"
fi

# 恢复配置文件
echo "⚙️  恢复配置文件..."
if [ -f "$BACKUP_DIR/${BACKUP_NAME}_config.env" ]; then
    cp "$BACKUP_DIR/${BACKUP_NAME}_config.env" .env
    echo "✅ 配置文件恢复完成"
else
    echo "⚠️  未找到配置文件备份"
fi

# 恢复日志文件
echo "📝 恢复日志文件..."
if [ -f "$BACKUP_DIR/${BACKUP_NAME}_logs.tar.gz" ]; then
    tar -xzf "$BACKUP_DIR/${BACKUP_NAME}_logs.tar.gz" -C . 2>/dev/null || echo "⚠️  日志文件恢复失败"
    echo "✅ 日志文件恢复完成"
else
    echo "⚠️  未找到日志文件备份"
fi

# 恢复应用数据
echo "📊 恢复应用数据..."
if [ -f "$BACKUP_DIR/${BACKUP_NAME}_data.tar.gz" ]; then
    tar -xzf "$BACKUP_DIR/${BACKUP_NAME}_data.tar.gz" -C . 2>/dev/null || echo "⚠️  应用数据恢复失败"
    echo "✅ 应用数据恢复完成"
else
    echo "⚠️  未找到应用数据备份"
fi

# 启动服务
echo "🚀 启动服务..."
docker-compose up -d

echo "🎉 数据恢复完成!"
echo "🔄 系统已重新启动"

# 显示服务状态
echo "📊 服务状态:"
docker-compose ps