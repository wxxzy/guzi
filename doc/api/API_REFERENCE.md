# 智投AI股票智能分析系统API文档

## 概述
智投AI股票智能分析系统提供了一套完整的RESTful API接口，允许开发者和第三方应用集成股票分析功能。API遵循标准的RESTful设计原则，使用JSON格式进行数据交换。

## 基础信息

### Base URL
```
生产环境: https://api.gushi-ai.com
开发环境: http://localhost:5000
```

### 认证方式
API使用API密钥进行认证，在请求头中添加:
```
Authorization: Bearer YOUR_API_KEY_HERE
```

### 请求格式
所有请求应使用`Content-Type: application/json`头部。

### 响应格式
所有响应均为JSON格式，包含以下字段：
```json
{
  "success": true,
  "data": {...},
  "message": "操作成功"
}
```

错误响应格式：
```json
{
  "success": false,
  "error": "错误信息",
  "code": "ERROR_CODE"
}
```

## 状态码说明

| 状态码 | 说明 |
|-------|------|
| 200 | 请求成功 |
| 400 | 请求参数错误 |
| 401 | 未授权访问 |
| 403 | 禁止访问 |
| 404 | 资源未找到 |
| 429 | 请求频率超限 |
| 500 | 服务器内部错误 |

## API接口列表

### 1. 股票数据接口

#### 获取股票列表
```
GET /api/stock/list
```

**请求参数:**
- `page` (可选): 页码，默认1
- `limit` (可选): 每页数量，默认20
- `sector` (可选): 行业筛选

**响应示例:**
```json
{
  "success": true,
  "data": [
    {
      "symbol": "000001",
      "name": "平安银行",
      "industry": "金融",
      "market_cap": 100000000000,
      "pe_ratio": 8.5,
      "pb_ratio": 0.8
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 1000
  }
}
```

#### 获取股票详情
```
GET /api/stock/{symbol}
```

**路径参数:**
- `symbol`: 股票代码

**响应示例:**
```json
{
  "success": true,
  "data": {
    "symbol": "000001",
    "name": "平安银行",
    "industry": "金融",
    "market_cap": 100000000000,
    "pe_ratio": 8.5,
    "pb_ratio": 0.8,
    "description": "平安银行是中国平安保险(集团)股份有限公司控股的全国性股份制商业银行。",
    "listed_date": "1991-04-03"
  }
}
```

#### 获取股票历史数据
```
GET /api/stock/{symbol}/history
```

**路径参数:**
- `symbol`: 股票代码

**查询参数:**
- `start_date` (可选): 开始日期，格式YYYY-MM-DD
- `end_date` (可选): 结束日期，格式YYYY-MM-DD

**响应示例:**
```json
{
  "success": true,
  "data": [
    {
      "date": "2023-01-01",
      "open_price": 10.5,
      "close_price": 11.2,
      "high_price": 11.5,
      "low_price": 10.3,
      "volume": 1000000,
      "turnover": 10500000
    }
  ]
}
```

### 2. 股票分析接口

#### 板块龙一龙二分析
```
POST /api/analysis/dragon
```

**请求体:**
```json
{
  "sector": "金融"  // 可选，不传则分析全市场
}
```

**响应示例:**
```json
{
  "success": true,
  "data": {
    "sector": "金融",
    "timestamp": "2023-10-07T10:00:00Z",
    "dragons": [
      {
        "symbol": "000001",
        "name": "平安银行",
        "industry": "金融",
        "market_cap": 100000000000,
        "pe_ratio": 8.5,
        "pb_ratio": 0.8,
        "score": 95.5
      }
    ],
    "analysis": "基于行业分类和多维度综合评分，平安银行在金融行业中排名第一..."
  }
}
```

#### 机构重仓股分析
```
POST /api/analysis/institutional
```

**请求体:**
```json
{
  "filters": {
    "min_market_cap": 50000000000,  // 最小市值50亿
    "min_roe": 0.08                 // 最小ROE 8%
  }
}
```

**响应示例:**
```json
{
  "success": true,
  "data": {
    "filters": {
      "min_market_cap": 50000000000,
      "min_roe": 0.08
    },
    "timestamp": "2023-10-07T10:00:00Z",
    "institutional_heavy_holding": [
      {
        "symbol": "000001",
        "name": "平安银行",
        "market_cap": 100000000000,
        "pe_ratio": 8.5,
        "pb_ratio": 0.8,
        "roe": 0.12,
        "score": 88.5
      }
    ],
    "analysis": "根据大市值、高ROE等机构偏好的筛选条件，平安银行符合机构重仓股特征..."
  }
}
```

#### 中小票龙头股分析
```
POST /api/analysis/small_cap_leader
```

**请求体:**
```json
{
  "max_market_cap": 10000000000  // 最大市值100亿
}
```

**响应示例:**
```json
{
  "success": true,
  "data": {
    "max_market_cap": 10000000000,
    "timestamp": "2023-10-07T10:00:00Z",
    "small_cap_leaders": [
      {
        "symbol": "002XXX",
        "name": "某科技公司",
        "market_cap": 5000000000,
        "pe_ratio": 25.0,
        "pb_ratio": 3.5,
        "score": 82.0
      }
    ],
    "analysis": "在市值100亿以下的股票中，该科技公司表现出较高的成长性和市场关注度..."
  }
}
```

#### 低估股票分析
```
POST /api/analysis/undervalued
```

**请求体:**
```json
{
  "criteria": {
    "pe_threshold": 15,  // PE阈值
    "pb_threshold": 1.5   // PB阈值
  }
}
```

**响应示例:**
```json
{
  "success": true,
  "data": {
    "criteria": {
      "pe_threshold": 15,
      "pb_threshold": 1.5
    },
    "timestamp": "2023-10-07T10:00:00Z",
    "undervalued_stocks": [
      {
        "symbol": "600XXX",
        "name": "某制造业公司",
        "pe_ratio": 12.0,
        "pb_ratio": 1.2,
        "score": 78.5
      }
    ],
    "analysis": "根据PE<15且PB<1.5的筛选条件，该制造业公司当前估值偏低..."
  }
}
```

### 3. AI智能分析接口

#### 个股深度分析
```
POST /api/analysis/{symbol}/ai
```

**路径参数:**
- `symbol`: 股票代码

**请求体:**
```json
{
  "type": "comprehensive"  // 分析类型: comprehensive, technical, fundamental
}
```

**响应示例:**
```json
{
  "success": true,
  "data": {
    "symbol": "000001",
    "analysis_type": "comprehensive",
    "ai_analysis": "【AI股票分析报告】

1. 基本面分析：
   - 公司财务状况良好，营收稳定增长
   - 盈利能力较强，ROE维持在行业平均水平之上
   - 资产负债结构合理，偿债能力较强

2. 技术面分析：
   - 当前价格处于上升通道中
   - 成交量配合良好，资金关注度较高
   - 技术指标显示短期有上涨动能

3. 估值分析：
   - 当前市盈率低于行业平均水平
   - 存在一定的估值修复空间
   - 长期价值被市场低估

4. 风险提示：
   - 宏观经济波动风险
   - 行业政策变化风险
   - 市场流动性风险

5. 投资建议：
   - 短期：谨慎观望
   - 中期：逢低布局
   - 长期：积极关注

注意：以上为AI分析结果，仅供参考。",
    "timestamp": "2023-10-07T10:00:00Z"
  }
}
```

#### 获取股票综合评分
```
POST /api/analysis/comprehensive_score
```

**请求体:**
```json
{
  "symbol": "000001"
}
```

**响应示例:**
```json
{
  "success": true,
  "data": {
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
}
```

#### 股票排名分析
```
POST /api/analysis/stock_ranking
```

**请求体:**
```json
{
  "limit": 20  // 返回前N只股票
}
```

**响应示例:**
```json
{
  "success": true,
  "data": {
    "limit": 20,
    "timestamp": "2023-10-07T10:00:00Z",
    "rankings": [
      {
        "symbol": "000001",
        "name": "平安银行",
        "comprehensive_score": 92.5,
        "technical_score": 88.0,
        "fundamental_score": 95.0,
        "valuation_score": 94.5,
        "rating": "强烈推荐"
      }
    ]
  }
}
```

### 4. 自然语言查询接口

#### 自然语言查询
```
POST /api/analysis/natural_language
```

**请求体:**
```json
{
  "query": "分析000001股票",
  "user_context": {
    "risk_tolerance": "medium",
    "investment_goal": "balanced"
  }
}
```

**响应示例:**
```json
{
  "success": true,
  "data": {
    "type": "stock_info",
    "symbols": ["000001"],
    "message": "正在查询股票 平安银行(000001) 的信息...",
    "query": "分析000001股票",
    "ai_analysis": "根据您的查询，平安银行(000001)是一只金融行业的优质股票..."
  }
}
```

### 5. 个性化推荐接口

#### 个性化推荐
```
POST /api/analysis/personalized_recommendation
```

**请求体:**
```json
{
  "user_profile": {
    "risk_tolerance": "medium",
    "investment_goal": "balanced",
    "investment_horizon": "medium",
    "capital_size": "medium",
    "investment_experience": "intermediate"
  }
}
```

**响应示例:**
```json
{
  "success": true,
  "data": {
    "timestamp": "2023-10-07T10:00:00Z",
    "user_profile": {
      "risk_tolerance": "medium",
      "investment_goal": "balanced"
    },
    "recommendation": "【AI个性化投资建议】

基于您的风险偏好和投资目标，为您推荐以下投资策略：

1. 资产配置建议：
   - 股票类资产：60%
   - 固定收益类：30%
   - 现金类：10%

2. 板块配置建议：
   - 科技板块：25%（重点关注人工智能、新能源）
   - 消费板块：20%（优选龙头企业）
   - 医疗板块：15%（长期价值投资）
   - 金融板块：10%（稳定收益）

3. 操作建议：
   - 采取分批建仓策略
   - 设置合理的止损止盈点
   - 保持长期投资理念

4. 风险管理：
   - 控制单一股票仓位不超20%
   - 定期调整投资组合
   - 关注宏观经济变化

免责说明：投资有风险，入市需谨慎。以上建议仅供参考，不构成投资建议。",
    "type": "personalized_recommendation"
  }
}
```

### 6. 情绪分析接口

#### 情绪分析
```
POST /api/analysis/sentiment_analysis
```

**请求体:**
```json
{
  "text": "这只股票表现不错，我很看好它的未来"
}
```

**响应示例:**
```json
{
  "success": true,
  "data": {
    "original_text": "这只股票表现不错，我很看好它的未来",
    "sentiment_analysis": "【情感分析结果】

情感倾向：积极
情感强度：8.5/10
情感标签：乐观、期待
关键情感词汇：不错、看好、未来
分析依据：文本中含有正面评价词汇'不错'和'看好'，表达了对未来表现的期待",
    "type": "sentiment_analysis"
  }
}
```

### 7. 市场整体分析接口

#### 市场趋势分析
```
GET /api/analysis/market_trend
```

**响应示例:**
```json
{
  "success": true,
  "data": {
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
    "market_sentiment": "neutral",
    "ai_analysis": "【市场整体趋势分析】

1. 市场整体表现：
   - 上证指数：2950.12点，涨幅0.45%
   - 深证成指：9567.28点，涨幅0.78%
   - 创业板指：2012.34点，涨幅1.12%

2. 行业表现：
   - 科技板块：+2.34%，领涨市场
   - 消费板块：+0.89%，稳步上涨
   - 金融板块：-0.23%，小幅回调
   - 医疗板块：+1.56%，表现强势

3. 市场情绪：中性偏乐观

4. 资金流向：主力资金净流入36.8亿元

5. 两市成交额：8970亿元，成交量维持高位

6. 后市展望：
   - 短期市场有望继续震荡上行
   - 关注政策面的进一步催化
   - 谨慎对待高位个股的回调风险"
  }
}
```

## 错误处理

### 常见错误码

| 错误码 | 说明 |
|-------|------|
| INVALID_REQUEST | 请求参数无效 |
| AUTHENTICATION_FAILED | 认证失败 |
| SERVICE_UNAVAILABLE | 服务不可用 |
| RATE_LIMIT_EXCEEDED | 请求频率超限 |
| STOCK_NOT_FOUND | 股票未找到 |
| ANALYSIS_FAILED | 分析失败 |
| INTERNAL_ERROR | 内部错误 |

### 错误响应示例
```json
{
  "success": false,
  "error": "请求参数无效：股票代码不能为空",
  "code": "INVALID_REQUEST"
}
```

## 速率限制

为保证服务质量，API对请求频率进行了限制：

- **默认限制**: 1000次/小时
- **分析类接口**: 100次/小时
- **AI服务接口**: 50次/小时

超过限制将返回429状态码。

## SDK支持

我们提供了多种编程语言的SDK来简化API调用：

### Python SDK
```python
from gushi_ai import GushiAIClient

client = GushiAIClient(api_key="YOUR_API_KEY")

# 获取股票列表
stocks = client.get_stock_list()

# AI分析股票
analysis = client.ai_analyze_stock("000001")
```

### JavaScript SDK
```javascript
import GushiAIClient from 'gushi-ai-sdk';

const client = new GushiAIClient({ apiKey: 'YOUR_API_KEY' });

// 获取股票列表
const stocks = await client.getStockList();

// AI分析股票
const analysis = await client.aiAnalyzeStock('000001');
```

## 最佳实践

### 1. 错误处理
始终检查API响应的成功状态，并妥善处理错误情况。

### 2. 速率限制
实现适当的重试机制和请求间隔，避免触发速率限制。

### 3. 数据缓存
对于不经常变化的数据，建议实现客户端缓存以减少API调用。

### 4. 异步处理
对于耗时较长的分析请求，建议使用异步处理方式。

### 5. 安全传输
始终使用HTTPS进行API调用，确保数据传输安全。

## 更新日志

### v1.0.0 (2025-10-07)
- 初始版本发布
- 实现基础股票数据接口
- 集成AI分析功能
- 提供完整的API文档

## 联系我们

如有任何问题或建议，请通过以下方式联系我们：

- **技术支持邮箱**: api-support@gushi-ai.com
- **开发者社区**: https://community.gushi-ai.com
- **API状态页面**: https://status.gushi-ai.com

---
© 2025 智投AI团队 版权所有