# guzi_backend/services/data_service.py

import akshare as ak
import pandas as pd
import redis
import json
import time

# --- 缓存配置 ---
CACHE_EXPIRATION_SECONDS = 3600  # 缓存1小时

# --- Redis 客户端 ---
redis_client = None
try:
    # 尝试初始化Redis客户端
    redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
    redis_client.ping() # 检查连接是否成功
    print("Successfully connected to Redis.")
except redis.exceptions.ConnectionError as e:
    print(f"Could not connect to Redis: {e}. Falling back to local in-memory cache.")
    redis_client = None

# --- 本地内存缓存 ---
local_cache = {}

def get_all_stocks():
    """
    获取所有A股的股票列表。
    优先从Redis缓存获取，如果Redis不可用，则使用本地内存缓存。
    
    Returns:
        pd.DataFrame: 包含股票代码和名称的DataFrame。
    """
    cache_key = "all_stocks_a_shares"

    # 1. 尝试从Redis缓存获取
    if redis_client:
        cached_data = redis_client.get(cache_key)
        if cached_data:
            print("Cache hit for all_stocks_a_shares in Redis.")
            stocks_list = json.loads(cached_data)
            return pd.DataFrame(stocks_list)
    
    # 2. 如果Redis不可用或未命中，尝试从本地缓存获取
    else:
        if cache_key in local_cache:
            cached_item = local_cache[cache_key]
            # 检查缓存是否过期
            if time.time() - cached_item['timestamp'] < CACHE_EXPIRATION_SECONDS:
                print("Cache hit for all_stocks_a_shares in local memory.")
                return cached_item['data']
            else:
                print("Local cache expired.")

    # 3. 如果所有缓存都未命中，则从数据源获取
    print("Cache miss. Fetching from AkShare.")
    try:
        # 使用已验证可行的接口获取A股代码和名称
        stocks_df = ak.stock_info_a_code_name()
        # stocks_df.rename(columns={'代码': 'code', '名称': 'name'}, inplace=True) # 新接口已是所需列名，无需重命名
        
        # 4. 将获取的数据存入缓存
        if redis_client:
            stocks_list = stocks_df.to_dict(orient='records')
            redis_client.setex(cache_key, CACHE_EXPIRATION_SECONDS, json.dumps(stocks_list))
            print(f"Cached {len(stocks_list)} stocks in Redis.")
        else:
            local_cache[cache_key] = {
                'data': stocks_df,
                'timestamp': time.time()
            }
            print(f"Cached {len(stocks_df)} stocks in local memory.")

        return stocks_df
    except Exception as e:
        print(f"Error fetching stock list from AkShare: {e}")
        return pd.DataFrame()
