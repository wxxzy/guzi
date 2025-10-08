# 生产环境部署指南

## 概述

本文档详细说明了如何在生产环境中部署基于AI大模型的股票智能分析系统。该系统采用Docker容器化部署，包含后端服务、数据库、缓存和前端应用四个核心组件。

## 部署架构

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│    前端应用      │    │    反向代理      │    │    后端服务      │
│  (React.js)     │◄──►│   (Nginx)       │◄──►│  (Flask)        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │                        │
        ┌─────────────────────┼────────────────────────┼─────────────────────┐
        ▼                     ▼                        ▼                     ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│    数据库        │    │    缓存服务      │    │    AI服务        │    │    监控服务      │
│  (PostgreSQL)   │    │   (Redis)       │    │  (通义千问等)    │    │  (Prometheus)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 系统要求

### 硬件要求
- **CPU**: 至少4核
- **内存**: 至少8GB RAM
- **存储**: 至少50GB可用磁盘空间
- **网络**: 稳定的互联网连接

### 软件要求
- **操作系统**: Linux (推荐Ubuntu 20.04+或CentOS 7+)
- **Docker**: 20.10.0+
- **Docker Compose**: 1.29.0+
- **Git**: 2.20.0+

## 部署步骤

### 1. 环境准备

```bash
# 更新系统包
sudo apt update && sudo apt upgrade -y

# 安装Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 安装Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 验证安装
docker --version
docker-compose --version
```

### 2. 项目获取

```bash
# 克隆项目代码
git clone <repository-url>
cd gushi

# 切换到生产分支（如果有）
git checkout production
```

### 3. 环境配置

```bash
# 复制环境配置文件模板
cp .env.example .env

# 编辑环境配置文件
nano .env
```

在`.env`文件中配置以下关键参数：

```bash
# Flask配置
FLASK_ENV=production
SECRET_KEY=your-secret-key-here-change-in-production

# 数据库配置
DB_PASSWORD=your-database-password-here
DB_USER=gushi_user
DB_NAME=gushi_db

# AI服务密钥
QWEN_API_KEY=your-qwen-api-key-here
VOLC_API_KEY=your-volc-api-key-here
OPENAI_API_KEY=your-openai-api-key-here

# 前端URL（用于CORS）
FRONTEND_URL=https://your-frontend-domain.com

# Redis配置
REDIS_PASSWORD=your-redis-password-here

# 日志级别
LOG_LEVEL=INFO

# API速率限制
API_RATE_LIMIT=1000 per hour

# 其他配置...
```

### 4. SSL证书配置（可选但推荐）

```bash
# 创建SSL目录
mkdir -p ssl

# 复制SSL证书文件（如果已有）
cp /path/to/your/certificate.crt ssl/
cp /path/to/your/private.key ssl/

# 或使用Let's Encrypt获取免费证书
sudo apt install certbot -y
sudo certbot certonly --standalone -d your-domain.com
```

### 5. 启动服务

```bash
# 构建并启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看服务日志
docker-compose logs -f
```

### 6. 数据库初始化

```bash
# 进入后端容器
docker-compose exec backend bash

# 在容器内执行数据库初始化
python init_db.py

# 退出容器
exit
```

### 7. 验证部署

```bash
# 检查后端服务
curl -v http://localhost:5000/health

# 检查前端服务
curl -v http://localhost:3000

# 检查数据库连接
docker-compose exec db psql -U gushi_user -d gushi_db -c "SELECT version();"

# 检查Redis连接
docker-compose exec redis redis-cli ping
```

## 配置详解

### 环境变量配置

#### Flask配置
- `FLASK_ENV`: 设置为`production`
- `SECRET_KEY`: 应用密钥，必须修改为强随机字符串

#### 数据库配置
- `DB_PASSWORD`: 数据库密码，必须修改
- `DB_USER`: 数据库用户名（默认:gushi_user）
- `DB_NAME`: 数据库名称（默认:gushi_db）

#### AI服务配置
- `QWEN_API_KEY`: 通义千问API密钥
- `VOLC_API_KEY`: 火山引擎API密钥
- `OPENAI_API_KEY`: OpenAI API密钥（如果使用）

#### 安全配置
- `FRONTEND_URL`: 前端应用URL，用于CORS限制
- `REDIS_PASSWORD`: Redis密码（如果配置）

#### 性能配置
- `API_RATE_LIMIT`: API请求速率限制

### Docker Compose配置

#### 后端服务 (backend)
- 使用Gunicorn作为WSGI服务器
- 4个工作进程
- 120秒超时时间

#### 数据库服务 (db)
- PostgreSQL 15-alpine
- 持久化数据卷
- 环境变量配置

#### 缓存服务 (redis)
- Redis 7-alpine
- 持久化数据卷

#### 反向代理 (nginx)
- Nginx alpine
- SSL支持
- 静态文件服务

#### 前端服务 (frontend)
- 基于Node.js的React应用
- 端口3000

## 监控与维护

### 系统监控

```bash
# 查看容器资源使用情况
docker stats

# 查看应用日志
docker-compose logs -f backend

# 查看Nginx访问日志
docker-compose logs -f nginx

# 查看数据库日志
docker-compose logs -f db
```

### 性能调优

#### 数据库优化
- 定期执行`VACUUM`和`ANALYZE`
- 监控慢查询日志
- 优化索引和查询

#### 应用优化
- 调整Gunicorn工作进程数
- 优化缓存策略
- 监控内存使用

#### 网络优化
- 使用CDN加速静态资源
- 启用Gzip压缩
- 优化SSL配置

### 备份与恢复

#### 数据库备份
```bash
# 创建备份脚本
#!/bin/bash
BACKUP_DIR="/backups"
DATE=$(date +"%Y%m%d_%H%M%S")
docker-compose exec db pg_dump -U gushi_user -d gushi_db > "$BACKUP_DIR/gushi_backup_$DATE.sql"

# 设置定时任务
crontab -e
# 添加: 0 2 * * * /path/to/backup_script.sh
```

#### 数据库恢复
```bash
# 停止应用
docker-compose stop backend

# 恢复数据库
docker-compose exec -T db psql -U gushi_user -d gushi_db < /backups/gushi_backup_*.sql

# 启动应用
docker-compose start backend
```

### 安全维护

#### 定期更新
```bash
# 更新Docker镜像
docker-compose pull

# 重建服务
docker-compose up -d --build
```

#### 安全扫描
```bash
# 扫描Docker镜像漏洞
docker scan backend

# 检查依赖安全
docker-compose exec backend pip-audit
```

#### 证书更新
```bash
# 更新SSL证书（如果使用Let's Encrypt）
sudo certbot renew --dry-run
```

## 故障排除

### 常见问题

#### 1. 服务无法启动
```bash
# 查看详细错误信息
docker-compose logs

# 检查容器状态
docker-compose ps

# 重新构建镜像
docker-compose build --no-cache
```

#### 2. 数据库连接失败
```bash
# 检查数据库服务状态
docker-compose ps db

# 查看数据库日志
docker-compose logs db

# 测试数据库连接
docker-compose exec db psql -U gushi_user -d gushi_db -c "SELECT 1;"
```

#### 3. AI服务调用失败
```bash
# 检查AI服务配置
grep -i "api_key" .env

# 查看后端日志
docker-compose logs backend | grep -i "ai\|qwen\|volc"

# 测试AI服务连接
docker-compose exec backend python -c "from ai_services.ai_client import test_ai_connection; print(test_ai_connection('qwen'))"
```

#### 4. 前端无法访问
```bash
# 检查前端服务状态
docker-compose ps frontend

# 查看前端日志
docker-compose logs frontend

# 检查Nginx配置
docker-compose exec nginx nginx -t
```

### 日志管理

```bash
# 查看所有服务日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f backend

# 限制日志大小
# 在docker-compose.yml中添加:
# logging:
#   driver: "json-file"
#   options:
#     max-size: "10m"
#     max-file: "3"
```

## 性能基准

### 响应时间
- API响应时间：< 2秒
- 页面加载时间：< 3秒
- 数据库查询：< 100毫秒

### 并发处理
- 支持100+并发用户
- 数据库连接池：20个连接
- Redis连接池：10个连接

### 资源使用
- 内存使用：< 1GB
- CPU使用：< 80%
- 磁盘使用：< 10GB（不含日志和备份）

## 升级与扩展

### 版本升级
```bash
# 获取最新代码
git pull origin production

# 重建服务
docker-compose build --no-cache

# 重启服务
docker-compose up -d

# 执行数据库迁移（如果需要）
docker-compose exec backend flask db upgrade
```

### 水平扩展
```bash
# 增加后端实例
docker-compose scale backend=3

# 增加前端实例
docker-compose scale frontend=2
```

### 垂直扩展
- 增加服务器资源（CPU、内存、存储）
- 调整Docker资源限制
- 优化数据库配置

## 结论

通过遵循本部署指南，您可以成功在生产环境中部署基于AI大模型的股票智能分析系统。该系统具备高可用性、高性能和安全性，能够为用户提供稳定、可靠的股票分析服务。

部署完成后，请定期进行系统维护和监控，确保系统的稳定运行。如遇到任何问题，请参考故障排除章节或联系技术支持。