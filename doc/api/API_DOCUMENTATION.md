# API接口文档

## 概述
本系统提供了一系列RESTful API接口，用于获取股票数据、执行分析任务和获取AI分析结果。

## 基础信息

### 基础URL
- 开发环境: `http://localhost:5000`
- 生产环境: `https://your-domain.com`

### 认证
目前API无需认证，但在生产环境中可能需要API密钥。

### 速率限制
- 默认限制: 每分钟1000次请求
- 特定接口可能有更严格的限制

## 接口列表

### 1. 健康检查接口

#### GET /health
检查应用健康状态

**请求示例:**
```bash
curl -X GET http://localhost:5000/health
```

**响应示例:**
```json
{
  "status": "healthy"
}
```

### 2. 股票数据接口

#### GET /api/stock/list
获取股票列表

**请求示例:**
```bash
curl -X GET http://localhost:5000/api/stock/list
```

**响应示例:**
```json
[
  {
    "id": 1,
    "symbol": "000001",
    "name": "平安银行",
    "industry": "金融",
    "market_cap": 100000000000,
    "pe_ratio": 8.5,
    "pb_ratio": 0.8
  }
]
```

#### GET /api/stock/{symbol}
获取特定股票详情

**请求示例:**
```bash
curl -X GET http://localhost:5000/api/stock/000001
```

**响应示例:**
```json
{
  "id": 1,
  "symbol": "000001",
  "name": "平安银行",
  "industry": "金融",
  "market_cap": 100000000000,
  "pe_ratio": 8.5,
  "pb_ratio": 0.8
}
```

#### GET /api/stock/{symbol}/history
获取股票历史数据

**请求参数:**
- start_date: 开始日期 (YYYY-MM-DD)
- end_date: 结束日期 (YYYY-MM-DD)

**请求示例:**
```bash
curl -X GET "http://localhost:5000/api/stock/000001/history?start_date=2023-01-01&end_date=2023-12-31"
```

**响应示例:**
```json
[
  {
    "id": 1,
    "stock_symbol": "000001",
    "date": "2023-01-01",
    "open_price": 10.5,
    "close_price": 11.2,
    "high_price": 11.5,
    "low_price": 10.3,
    "volume": 1000000
  }
]
```

### 3. 股票分析接口

#### POST /api/analysis/dragon
板块龙一龙二分析

**请求参数:**
- sector: 行业板块 (可选)

**请求示例:**
```bash
curl -X POST http://localhost:5000/api/analysis/dragon \
  -H "Content-Type: application/json" \
  -d '{"sector": "金融"}'
```

**响应示例:**
```json
{
  "sector": "金融",
  "timestamp": "2023-10-07T10:00:00Z",
  "dragons": [
    {
      "id": 1,
      "symbol": "000001",
      "name": "平安银行",
      "industry": "金融",
      "market_cap": 100000000000,
      "pe_ratio": 8.5,
      "pb_ratio": 0.8
    }
  ],
  "top_stocks": [...]
}
```

#### POST /api/analysis/institutional
机构重仓股分析

**请求参数:**
- filters: 筛选条件 (可选)

**请求示例:**
```bash
curl -X POST http://localhost:5000/api/analysis/institutional \
  -H "Content-Type: application/json" \
  -d '{"filters": {"min_market_cap": 50000000000}}'
```

**响应示例:**
```json
{
  "filters": {"min_market_cap": 50000000000},
  "timestamp": "2023-10-07T10:00:00Z",
  "institutional_heavy_holding": [...]
}
```

#### POST /api/analysis/small_cap_leader
中小票龙头股分析

**请求参数:**
- max_market_cap: 最大市值 (可选，默认100亿)

**请求示例:**
```bash
curl -X POST http://localhost:5000/api/analysis/small_cap_leader \
  -H "Content-Type: application/json" \
  -d '{"max_market_cap": 10000000000}'
```

**响应示例:**
```json
{
  "max_market_cap": 10000000000,
  "timestamp": "2023-10-07T10:00:00Z",
  "small_cap_leaders": [...]
}
```

#### POST /api/analysis/undervalued
低估股票分析

**请求参数:**
- criteria: 筛选条件 (可选)

**请求示例:**
```bash
curl -X POST http://localhost:5000/api/analysis/undervalued \
  -H "Content-Type: application/json" \
  -d '{"criteria": {"pe_threshold": 15, "pb_threshold": 1.5}}'
```

**响应示例:**
```json
{
  "criteria": {"pe_threshold": 15, "pb_threshold": 1.5},
  "timestamp": "2023-10-07T10:00:00Z",
  "undervalued_stocks": [...]
}
```

### 4. AI分析接口

#### POST /api/analysis/{symbol}/ai
使用AI进行个股深度分析

**请求参数:**
- type: 分析类型 (comprehensive, technical, fundamental)

**请求示例:**
```bash
curl -X POST http://localhost:5000/api/analysis/000001/ai \
  -H "Content-Type: application/json" \
  -d '{"type": "comprehensive"}'
```

**响应示例:**
```json
{
  "symbol": "000001",
  "analysis_type": "comprehensive",
  "ai_analysis": "详细的AI分析结果...",
  "timestamp": "2023-10-07T10:00:00Z"
}
```

#### POST /api/analysis/comprehensive_score
获取股票综合评分

**请求参数:**
- symbol: 股票代码

**请求示例:**
```bash
curl -X POST http://localhost:5000/api/analysis/comprehensive_score \
  -H "Content-Type: application/json" \
  -d '{"symbol": "000001"}'
```

**响应示例:**
```json
{
  "symbol": "000001",
  "comprehensive_analysis": {
    "technical_score": 75.5,
    "fundamental_score": 82.3,
    "valuation_score": 68.7,
    "comprehensive_score": 75.5,
    "rating": "推荐"
  },
  "timestamp": "2023-10-07T10:00:00Z"
}
```

#### POST /api/analysis/stock_ranking
获取股票排名

**请求参数:**
- limit: 限制数量 (可选，默认20)

**请求示例:**
```bash
curl -X POST http://localhost:5000/api/analysis/stock_ranking \
  -H "Content-Type: application/json" \
  -d '{"limit": 10}'
```

**响应示例:**
```json
{
  "rankings": [...],
  "timestamp": "2023-10-07T10:00:00Z"
}
```

#### POST /api/analysis/natural_language
自然语言查询

**请求参数:**
- query: 查询语句
- user_context: 用户上下文 (可选)

**请求示例:**
```bash
curl -X POST http://localhost:5000/api/analysis/natural_language \
  -H "Content-Type: application/json" \
  -d '{"query": "分析000001股票", "user_context": {}}'
```

**响应示例:**
```json
{
  "type": "stock_info",
  "symbols": ["000001"],
  "message": "正在查询股票 平安银行(000001) 的信息...",
  "query": "分析000001股票"
}
```

#### POST /api/analysis/personalized_recommendation
个性化推荐

**请求参数:**
- user_profile: 用户画像

**请求示例:**
```bash
curl -X POST http://localhost:5000/api/analysis/personalized_recommendation \
  -H "Content-Type: application/json" \
  -d '{"user_profile": {"risk_tolerance": "medium", "investment_goal": "balanced"}}'
```

**响应示例:**
```json
{
  "timestamp": "2023-10-07T10:00:00Z",
  "user_profile": {"risk_tolerance": "medium", "investment_goal": "balanced"},
  "recommendation": "个性化推荐结果...",
  "type": "personalized_recommendation"
}
```

#### GET /api/analysis/market_trend
分析市场整体趋势

**请求示例:**
```bash
curl -X GET http://localhost:5000/api/analysis/market_trend
```

**响应示例:**
```json
{
  "timestamp": "2023-10-07T10:00:00Z",
  "market_trend": "bullish",
  "key_indicators": {
    "shanghai_index": 2950.12,
    "shenzhen_index": 9567.28,
    "growth_index": 2012.34
  },
  "sector_performance": {
    "technology": 2.5,
    "healthcare": 1.8,
    "finance": -0.2,
    "consumer": 0.9
  },
  "market_sentiment": "neutral"
}
```

### 5. 监控接口

#### GET /monitoring/health
监控健康检查

**请求示例:**
```bash
curl -X GET http://localhost:5000/monitoring/health
```

#### GET /monitoring/metrics
获取监控指标

**请求示例:**
```bash
curl -X GET http://localhost:5000/monitoring/metrics
```

#### GET /monitoring/alerts
获取警报历史

**请求示例:**
```bash
curl -X GET http://localhost:5000/monitoring/alerts
```

#### GET /monitoring/status
获取系统状态

**请求示例:**
```bash
curl -X GET http://localhost:5000/monitoring/status
```

## 错误响应格式

所有错误响应都遵循统一格式：

```json
{
  "error": "错误描述",
  "message": "详细错误信息"
}
```

## 状态码说明

- 200: 请求成功
- 400: 请求参数错误
- 404: 资源未找到
- 429: 请求过于频繁
- 500: 服务器内部错误

## 示例代码

### Python示例
```python
import requests

# 获取股票列表
response = requests.get('http://localhost:5000/api/stock/list')
stocks = response.json()

# 分析龙一龙二
payload = {'sector': '金融'}
response = requests.post('http://localhost:5000/api/analysis/dragon', json=payload)
dragon_analysis = response.json()

# AI个股分析
payload = {'type': 'comprehensive'}
response = requests.post('http://localhost:5000/api/analysis/000001/ai', json=payload)
ai_analysis = response.json()
```

### JavaScript示例
```javascript
// 获取股票列表
fetch('http://localhost:5000/api/stock/list')
  .then(response => response.json())
  .then(stocks => console.log(stocks));

// 分析龙一龙二
fetch('http://localhost:5000/api/analysis/dragon', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({sector: '金融'}),
})
  .then(response => response.json())
  .then(data => console.log(data));

// AI个股分析
fetch('http://localhost:5000/api/analysis/000001/ai', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({type: 'comprehensive'}),
})
  .then(response => response.json())
  .then(data => console.log(data));
```