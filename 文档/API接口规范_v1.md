# 股票智能分析系统 - API接口规范 v1

## 1. 基本原则

- **Base URL**: 所有API都以 `/api/v1` 为前缀。
- **数据格式**: 所有请求体和响应体都使用 `application/json` 格式。
- **认证**: 除登录注册等公开接口外，所有需要授权的API都必须在HTTP请求头中携带 `Authorization: Bearer <token>`。
- **命名**: URL路径使用小写字母和连字符 `-`，参数使用蛇形命名法 `snake_case`。

## 2. 认证

系统采用基于 JWT (JSON Web Token) 的无状态认证机制。

- **登录接口**: `POST /api/v1/auth/login`
- **成功响应**: 返回一个包含 `access_token` 的JSON对象。
- **Token有效期**: Access Token 有效期为24小时。

## 3. 通用响应格式

所有API响应都应遵循统一的结构，方便客户端处理。

**成功响应 (`200 OK`)**
```json
{
  "code": 0,
  "message": "Success",
  "data": { ... } // 具体的业务数据
}
```

**失败响应 (`4xx` or `5xx`)**
```json
{
  "code": 40001, // 业务错误码
  "message": "Invalid parameter: username cannot be empty.", // 错误信息
  "data": null
}
```

## 4. 核心API端点

### 4.1. 用户认证 (`/auth`)

- **用户注册**
    - **Endpoint**: `POST /api/v1/auth/register`
    - **描述**: 创建一个新用户。
    - **请求体**:
      ```json
      {
        "username": "newuser",
        "password": "password123",
        "email": "user@example.com"
      }
      ```
    - **响应 (201)**:
      ```json
      {
        "code": 0,
        "message": "User created successfully.",
        "data": {
          "user_id": 1,
          "username": "newuser"
        }
      }
      ```

- **用户登录**
    - **Endpoint**: `POST /api/v1/auth/login`
    - **描述**: 用户登录并获取JWT。
    - **请求体**:
      ```json
      {
        "username": "newuser",
        "password": "password123"
      }
      ```
    - **响应 (200)**:
      ```json
      {
        "code": 0,
        "message": "Login successful.",
        "data": {
          "access_token": "ey..."
        }
      }
      ```

### 4.2. 股票数据 (`/stocks`)

- **获取股票列表**
    - **Endpoint**: `GET /api/v1/stocks`
    - **描述**: 获取股票列表，支持分页和筛选。
    - **查询参数**:
        - `page` (int, optional, default: 1): 页码
        - `per_page` (int, optional, default: 20): 每页数量
        - `market` (string, optional): 市场代码, e.g., `SH`
    - **响应 (200)**:
      ```json
      {
        "code": 0,
        "message": "Success",
        "data": {
          "stocks": [
            { "code": "600519.SH", "name": "贵州茅台" },
            { "code": "000001.SZ", "name": "平安银行" }
          ],
          "pagination": { "total": 5000, "page": 1, "per_page": 20 }
        }
      }
      ```

- **获取单只股票日线数据**
    - **Endpoint**: `GET /api/v1/stocks/{code}/kline`
    - **描述**: 获取指定股票的K线（日线）数据。
    - **路径参数**: `code` (string, required): 股票代码, e.g., `600519.SH`
    - **查询参数**:
        - `start_date` (string, optional, format: YYYY-MM-DD)
        - `end_date` (string, optional, format: YYYY-MM-DD)
    - **响应 (200)**:
      ```json
      {
        "code": 0,
        "message": "Success",
        "data": [
          { "date": "2023-10-01", "open": 1700.00, "close": 1720.50, ... },
          { "date": "2023-10-02", "open": 1721.00, "close": 1730.00, ... }
        ]
      }
      ```

### 4.3. 分析服务 (`/analysis`)

- **请求板块龙头分析**
    - **Endpoint**: `POST /api/v1/analysis/dragon-head`
    - **描述**: 对指定板块进行龙头分析。
    - **请求体**:
      ```json
      {
        "industry": "白酒"
      }
      ```
    - **响应 (200)**:
      ```json
      {
        "code": 0,
        "message": "Success",
        "data": {
          "dragon_one": { "code": "600519.SH", "name": "贵州茅台", "score": 98.5 },
          "dragon_two": { "code": "000858.SZ", "name": "五粮液", "score": 95.2 }
        }
      }
      ```

### 4.4. 用户自选股 (`/watchlist`)

- **获取我的自选股**
    - **Endpoint**: `GET /api/v1/watchlist`
    - **描述**: 获取当前用户的自选股列表。
    - **响应 (200)**:
      ```json
      {
        "code": 0,
        "message": "Success",
        "data": [
          { "code": "600519.SH", "name": "贵州茅台", "added_at": "..." }
        ]
      }
      ```

- **添加自选股**
    - **Endpoint**: `POST /api/v1/watchlist`
    - **请求体**:
      ```json
      {
        "stock_code": "000001.SZ"
      }
      ```
    - **响应 (201)**: `204 No Content`

- **移除自选股**
    - **Endpoint**: `DELETE /api/v1/watchlist/{code}`
    - **路径参数**: `code` (string, required): 股票代码
    - **响应 (200)**: `204 No Content`
