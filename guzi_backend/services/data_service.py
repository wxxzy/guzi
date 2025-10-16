# guzi_backend/services/data_service.py

import akshare as ak
import pandas as pd
import redis
import json
import time

from ..database import db
from ..models import Stock

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

def _get_from_cache(key: str):
    if redis_client:
        cached_data = redis_client.get(key)
        if cached_data:
            print(f"Cache hit for {key} in Redis.")
            return json.loads(cached_data)
    else:
        if key in local_cache:
            cached_item = local_cache[key]
            if time.time() - cached_item['timestamp'] < CACHE_EXPIRATION_SECONDS:
                print(f"Cache hit for {key} in local memory.")
                return cached_item['data']
    return None

def _set_to_cache(key: str, data):
    if redis_client:
        try:
            redis_client.setex(key, CACHE_EXPIRATION_SECONDS, json.dumps(data))
            print(f"Cached {key} in Redis.")
        except redis.exceptions.ConnectionError as e:
            print(f"Redis connection error, could not cache {key}: {e}")
    else:
        local_cache[key] = {
            'data': data,
            'timestamp': time.time()
        }
        print(f"Cached {key} in local memory.")

def get_all_stocks():
    """
    获取所有A股的股票列表。
    优先从缓存获取，如果缓存中没有，则通过akshare获取并存入缓存。
    
    Returns:
        pd.DataFrame: 包含股票代码和名称的DataFrame。
    """
    cache_key = "all_stocks_a_shares"
    cached_data = _get_from_cache(cache_key)
    if cached_data:
        return pd.DataFrame(cached_data)

    print("Cache miss. Fetching from AkShare.")
    try:
        stocks_df = ak.stock_info_a_code_name()
        _set_to_cache(cache_key, stocks_df.to_dict(orient='records'))
        return stocks_df
    except Exception as e:
        print(f"Error fetching stock list from AkShare: {e}")
        return pd.DataFrame()

def fetch_stock_industry_map():
    """
    获取股票代码到行业名称的映射。
    优先从缓存获取，如果缓存中没有，则通过akshare获取并存入缓存。
    
    Returns:
        dict: 股票代码到行业名称的映射字典。
    """
    cache_key = "stock_industry_map"
    cached_data = _get_from_cache(cache_key)
    if cached_data:
        return cached_data

    print("Cache miss. Fetching industry data from AkShare.")
    stock_industry_map = {}
    try:
        # 1. 获取所有行业板块名称
        industry_names_df = ak.stock_board_industry_name_em()
        if industry_names_df.empty:
            print("Failed to fetch industry names.")
            return {}

        # 2. 遍历每个行业，获取其成分股
        for index, row in industry_names_df.iterrows():
            industry_name = row['板块名称']
            try:
                # 获取行业成分股，可能需要一些时间
                cons_df = ak.stock_board_industry_cons_em(symbol=industry_name)
                if not cons_df.empty:
                    for _, cons_row in cons_df.iterrows():
                        stock_code = cons_row['代码']
                        stock_industry_map[stock_code] = industry_name
            except Exception as e:
                print(f"Error fetching constituents for {industry_name}: {e}")
                continue
        
        _set_to_cache(cache_key, stock_industry_map)
        return stock_industry_map

    except Exception as e:
        print(f"Error fetching industry data from AkShare: {e}")
        return {}


def update_stock_list_in_db():
    """
    从数据源获取最新股票列表和行业信息，并更新到数据库中。
    """
    print("Fetching latest stock list to update database...")
    stocks_df = get_all_stocks()
    stock_industry_map = fetch_stock_industry_map()

    if stocks_df.empty:
        print("Failed to fetch stock list. Database update skipped.")
        return

    count = 0
    for index, row in stocks_df.iterrows():
        stock_code = row['code']
        stock_name = row['name']
        industry = stock_industry_map.get(stock_code, None) # 从映射中获取行业信息

        stock_obj = Stock(
            code=stock_code,
            name=stock_name,
            industry=industry, # 填充行业信息
            market='A-Share' 
        )
        db.session.merge(stock_obj)
        count += 1

    db.session.commit()
    print(f"Database update complete. {count} stock records processed.")
