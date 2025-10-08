# 智投AI股票智能分析系统

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0%2B-green)](https://flask.palletsprojects.com/)
[![React](https://img.shields.io/badge/React-18.0%2B-blue)](https://reactjs.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

## 项目简介

智投AI股票智能分析系统是一个基于AI大模型的股票智能分析平台，利用通义千问、火山引擎等AI大模型技术，结合AkShare金融数据源，为投资者提供专业的股票分析和投资建议。

系统能够分析股市每个板块的过往龙一龙二、机构重仓股、中小票龙头股、小票热门股以及当前被低估的股票。

## 核心功能

### 📊 股票智能分析
- **板块龙一龙二识别** - 分析各行业的龙头股票
- **机构重仓股分析** - 识别基金等机构重仓持有的股票
- **中小票龙头股识别** - 发现小市值但表现突出的股票
- **小票热门股识别** - 识别当前市场关注度高的小市值股票
- **低估股票识别** - 基于基本面指标识别被低估的股票

### 🤖 AI智能分析
- **AI驱动分析** - 支持通义千问、火山引擎等多个大模型服务
- **自然语言查询** - 支持自然语言的股票查询和分析
- **个性化推荐** - 根据用户画像提供个性化投资建议
- **市场整体分析** - 提供市场概况和板块分析

### 📈 数据可视化
- **技术面分析** - K线图、技术指标等可视化展示
- **基本面分析** - 财务数据对比和趋势分析
- **估值分析** - 估值水平和历史对比
- **行业分布** - 行业股票分布和表现分析

## 技术架构

### 后端技术栈
- **框架**: Flask + Flask-RESTful
- **数据库**: SQLite/PostgreSQL + SQLAlchemy
- **AI服务**: 通义千问、火山引擎、OpenAI兼容API
- **数据源**: AkShare金融数据接口
- **部署**: Docker + Docker Compose

### 前端技术栈
- **框架**: React 18 + Hooks
- **状态管理**: Redux/Zustand
- **UI组件**: Ant Design/Bootstrap
- **数据可视化**: Recharts/ECharts
- **构建工具**: Vite/Webpack

## 快速开始

### 环境要求
- Python 3.8+
- Node.js 14+
- Docker (可选，用于容器化部署)
- PostgreSQL (生产环境)

### 后端部署

```bash
# 克隆项目
git clone <repository-url>
cd gushi_backend

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填写API密钥等配置

# 初始化数据库
python init_db.py

# 启动服务
python app.py
```

### 前端部署

```bash
# 进入前端目录
cd gushi_frontend

# 安装依赖
npm install

# 启动开发服务器
npm start

# 构建生产版本
npm run build
```

### Docker部署

```bash
# 构建并启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

## API接口文档

完整的API文档请参见 [API参考文档](doc/api/API_REFERENCE.md)

## 配置说明

### 环境变量配置

在 `.env` 文件中配置以下变量：

```bash
# Flask配置
FLASK_ENV=production
SECRET_KEY=your-secret-key-here

# 数据库配置
DATABASE_URL=postgresql://user:password@localhost/dbname

# AI服务密钥
QWEN_API_KEY=your-qwen-api-key
VOLC_API_KEY=your-volc-api-key
OPENAI_API_KEY=your-openai-api-key

# 数据源配置
AKSHARE_TOKEN=your-akshare-token

# 其他配置
FRONTEND_URL=https://your-frontend-domain.com
```

## 开发指南

### 项目结构

```
gushi/
├── gushi_backend/          # 后端代码
│   ├── ai_services/       # AI服务模块
│   ├── data_source/        # 数据源模块
│   ├── models/            # 数据模型
│   ├── routes/            # API路由
│   ├── services/          # 业务逻辑服务
│   ├── security/          # 安全模块
│   ├── monitoring/        # 监控模块
│   ├── tests/            # 测试代码
│   ├── app.py            # 应用入口
│   └── config.py         # 配置文件
├── gushi_frontend/        # 前端代码
│   ├── src/              # 源代码
│   │   ├── components/   # 组件
│   │   ├── pages/        # 页面
│   │   ├── services/     # API服务
│   │   └── utils/        # 工具函数
│   └── public/           # 静态资源
├── docker-compose.yml    # Docker编排文件
└── README.md            # 项目文档
```

### 开发环境搭建

```bash
# 后端开发环境
cd gushi_backend
pip install -r requirements-dev.txt

# 运行单元测试
python -m pytest tests/

# 前端开发环境
cd gushi_frontend
npm install
npm start
```

## 测试

### 单元测试
```bash
cd gushi_backend
python -m pytest tests/unit_tests.py -v
```

### 集成测试
```bash
cd gushi_backend
python -m pytest tests/integration_tests.py -v
```

### 性能测试
```bash
cd gushi_backend
python -m pytest tests/performance_tests.py -v
```

## 监控与运维

### 健康检查
- `GET /health` - 应用健康检查
- `GET /monitoring/health` - 详细健康检查
- `GET /monitoring/metrics` - 系统指标

### 日志管理
- 应用日志存储在 `/var/log/gushi/`
- 支持日志轮转和归档
- 提供日志查询API

### 告警机制
- 系统异常自动告警
- 性能阈值告警
- 支持邮件、Webhook等多种通知方式

## 安全特性

### 认证授权
- JWT Token认证
- API密钥验证
- 角色权限控制

### 数据安全
- 敏感数据加密存储
- SQL注入防护
- XSS攻击防护

### 网络安全
- HTTPS强制使用
- CORS安全配置
- 请求频率限制

## 性能优化

### 缓存策略
- Redis缓存热点数据
- 数据库查询结果缓存
- API响应缓存

### 数据库优化
- 索引优化
- 查询优化
- 连接池管理

### 前端优化
- 代码分割
- 懒加载
- CDN加速

## 贡献指南

我们欢迎任何形式的贡献！

### 提交Issue
1. 在GitHub上提交Issue
2. 详细描述问题或建议
3. 提供复现步骤（如果是Bug）

### 提交Pull Request
1. Fork项目仓库
2. 创建功能分支
3. 提交代码更改
4. 编写测试用例
5. 提交Pull Request

### 代码规范
- 遵循PEP8 Python代码规范
- 使用类型提示
- 编写单元测试
- 添加必要的文档注释

## 文档

- [项目概述](doc/PROJECT_OVERVIEW.md)
- [架构设计](doc/ARCHITECTURE.md)
- [API参考](doc/api/API_REFERENCE.md)
- [用户手册](doc/user_guide/USER_MANUAL.md)
- [部署指南](doc/deployment/PRODUCTION_DEPLOYMENT_GUIDE.md)
- [开发指南](doc/DEVELOPMENT_GUIDE.md)

## 许可证

本项目采用MIT许可证，详情请见[LICENSE](LICENSE)文件。

## 联系方式

如有任何问题或建议，请通过以下方式联系我们：

- 邮箱: [support@gushi-ai.com](mailto:support@gushi-ai.com)
- GitHub Issues: [项目Issues页面](https://github.com/your-username/gushi/issues)

---

**免责声明**: 本系统提供的分析结果仅供参考，不构成投资建议。投资有风险，入市需谨慎。