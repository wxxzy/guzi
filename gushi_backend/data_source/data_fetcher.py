import akshare as ak
import pandas as pd
from datetime import datetime, timedelta
from models import Stock, StockData, db
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_stock_data(symbol, start_date=None, end_date=None):
    """
    获取股票数据
    :param symbol: 股票代码
    :param start_date: 开始日期
    :param end_date: 结束日期
    :return: 股票数据
    """
    try:
        # 如果没有指定日期，默认获取最近一年的数据
        if not end_date:
            end_date = datetime.now().strftime('%Y%m%d')
        if not start_date:
            start_date = (datetime.now() - timedelta(days=365)).strftime('%Y%m%d')
        
        # 使用akshare获取股票历史数据
        stock_data = ak.stock_zh_a_hist(symbol=symbol, period="daily", start_date=start_date, end_date=end_date, adjust="")
        
        if stock_data is not None and not stock_data.empty:
            # 重命名列以匹配数据库模型
            column_mapping = {
                '日期': 'date',
                '开盘': 'open_price',
                '收盘': 'close_price',
                '最高': 'high_price',
                '最低': 'low_price',
                '成交量': 'volume'
            }
            stock_data = stock_data.rename(columns=column_mapping)
            
            # 转换日期格式
            stock_data['date'] = pd.to_datetime(stock_data['date']).dt.date
            
            # 处理成交量单位（akshare返回的是手，转换为实际成交量）
            stock_data['volume'] = pd.to_numeric(stock_data['volume'], errors='coerce')
            
            logger.info(f"成功获取股票 {symbol} 的 {len(stock_data)} 条历史数据")
            return stock_data
        else:
            logger.warning(f"未获取到股票 {symbol} 的数据")
            return pd.DataFrame()  # 返回空DataFrame而不是None
    except Exception as e:
        logger.error(f"获取股票数据失败: {str(e)}")
        return pd.DataFrame()  # 返回空DataFrame而不是None

def fetch_stock_info(symbol):
    """
    获取股票基本信息
    :param symbol: 股票代码
    :return: 股票基本信息
    """
    try:
        # 获取A股实时行情数据
        stock_info = ak.stock_zh_a_spot_em()
        
        # 筛选指定股票
        stock_row = stock_info[stock_info['代码'] == symbol]
        
        if not stock_row.empty:
            return {
                'symbol': symbol,
                'name': stock_row.iloc[0]['名称'],
                'current_price': float(stock_row.iloc[0]['最新价']) if pd.notna(stock_row.iloc[0]['最新价']) else None,
                'change_percent': float(stock_row.iloc[0]['涨跌幅']) if pd.notna(stock_row.iloc[0]['涨跌幅']) else None,
                'change_amount': float(stock_row.iloc[0]['涨跌额']) if pd.notna(stock_row.iloc[0]['涨跌额']) else None,
                'volume': int(stock_row.iloc[0]['成交量']) if pd.notna(stock_row.iloc[0]['成交量']) else None,
                'turnover': float(stock_row.iloc[0]['成交额']) if pd.notna(stock_row.iloc[0]['成交额']) else None,
                'market_cap': float(stock_row.iloc[0]['总市值']) if pd.notna(stock_row.iloc[0]['总市值']) else None
            }
        else:
            logger.warning(f"未找到股票 {symbol} 的信息")
            return None
    except Exception as e:
        logger.error(f"获取股票信息失败: {str(e)}")
        return None

def sync_stock_list():
    """
    同步股票列表到数据库
    """
    try:
        logger.info("开始同步股票列表...")
        
        # 获取沪深京A股列表
        try:
            stock_info_sh = ak.stock_info_sh_name_code()  # 上海A股
        except Exception as e:
            logger.warning(f"获取上海A股列表失败: {str(e)}")
            stock_info_sh = pd.DataFrame()
            
        try:
            stock_info_sz = ak.stock_info_sz_name_code()  # 深圳A股
        except Exception as e:
            logger.warning(f"获取深圳A股列表失败: {str(e)}")
            stock_info_sz = pd.DataFrame()
            
        try:
            stock_info_bj = ak.stock_info_bj_name_code()  # 北京A股
        except Exception as e:
            logger.warning(f"获取北京A股列表失败: {str(e)}")
            stock_info_bj = pd.DataFrame()
        
        # 合并所有股票信息
        all_stocks = pd.concat([stock_info_sh, stock_info_sz, stock_info_bj], ignore_index=True)
        
        added_count = 0
        updated_count = 0
        
        for _, row in all_stocks.iterrows():
            symbol = str(row.get('code', row.get('证券代码', ''))).strip()
            name = str(row.get('name', row.get('证券简称', ''))).strip()
            industry = str(row.get('industry', row.get('所属行业', ''))).strip()
            
            if not symbol or symbol == '':
                continue
                
            # 检查是否已存在
            existing_stock = Stock.query.filter_by(symbol=symbol).first()
            
            if existing_stock:
                # 更新现有股票信息
                existing_stock.name = name
                existing_stock.industry = industry if industry != '' else existing_stock.industry
                updated_count += 1
            else:
                # 创建新股票记录
                new_stock = Stock(symbol=symbol, name=name, industry=industry if industry != '' else None)
                db.session.add(new_stock)
                added_count += 1
        
        db.session.commit()
        logger.info(f"股票列表同步完成: 新增 {added_count} 只，更新 {updated_count} 只")
        
        return {
            'added': added_count,
            'updated': updated_count,
            'total': len(all_stocks)
        }
    except Exception as e:
        db.session.rollback()
        logger.error(f"同步股票列表失败: {str(e)}")
        return {'error': str(e)}

def fetch_sector_stocks(sector):
    """
    获取指定行业的股票列表
    :param sector: 行业名称
    :return: 该行业股票列表
    """
    try:
        # 获取行业成分股信息
        stocks = Stock.query.filter(Stock.industry.like(f'%{sector}%')).all()
        logger.info(f"获取行业 {sector} 的股票 {len(stocks)} 只")
        return stocks
    except Exception as e:
        logger.error(f"获取行业股票列表失败: {str(e)}")
        return []

def fetch_financial_indicators(symbol):
    """
    获取股票财务指标
    :param symbol: 股票代码
    :return: 财务指标
    """
    try:
        # 获取个股F9财务信息
        # 注意：akshare的财务数据接口可能需要根据实际情况调整
        # 这里使用通用的财务指标获取方法
        stock_profile = ak.stock_profile_cninfo(symbol=symbol)
        if stock_profile is not None:
            return stock_profile
        
        # 如果上面的方法不成功，尝试其他接口
        # 获取个股基本信息
        stock_info = ak.stock_individual_info_em(symbol=symbol)
        return stock_info
    except Exception as e:
        logger.error(f"获取股票 {symbol} 财务指标失败: {str(e)}")
        return None

def sync_historical_data(symbol, days=365):
    """
    同步特定股票的历史数据到数据库
    :param symbol: 股票代码
    :param days: 同步天数
    """
    try:
        logger.info(f"开始同步股票 {symbol} 的历史数据...")
        
        # 计算日期范围
        end_date = datetime.now().strftime('%Y%m%d')
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y%m%d')
        
        # 获取历史数据
        stock_data = fetch_stock_data(symbol, start_date, end_date)
        
        if stock_data.empty:
            logger.warning(f"未获取到股票 {symbol} 的历史数据")
            return {'success': False, 'message': '未获取到数据'}
        
        # 将数据同步到数据库
        added_count = 0
        updated_count = 0
        
        for _, row in stock_data.iterrows():
            # 检查数据库中是否已存在该日期的数据
            existing_data = StockData.query.filter(
                StockData.stock_symbol == symbol,
                StockData.date == row['date']
            ).first()
            
            if existing_data:
                # 更新现有数据
                existing_data.open_price = row['open_price']
                existing_data.close_price = row['close_price']
                existing_data.high_price = row['high_price']
                existing_data.low_price = row['low_price']
                existing_data.volume = row['volume']
                updated_count += 1
            else:
                # 创建新数据记录
                new_data = StockData(
                    stock_symbol=symbol,
                    date=row['date'],
                    open_price=row['open_price'],
                    close_price=row['close_price'],
                    high_price=row['high_price'],
                    low_price=row['low_price'],
                    volume=row['volume']
                )
                db.session.add(new_data)
                added_count += 1
        
        db.session.commit()
        logger.info(f"股票 {symbol} 历史数据同步完成: 新增 {added_count} 条，更新 {updated_count} 条")
        
        return {
            'success': True,
            'added': added_count,
            'updated': updated_count
        }
    except Exception as e:
        db.session.rollback()
        logger.error(f"同步股票 {symbol} 历史数据失败: {str(e)}")
        return {'success': False, 'error': str(e)}

def get_market_data_summary():
    """
    获取市场整体数据摘要
    """
    try:
        # 获取市场整体行情
        market_data = ak.stock_zh_a_spot_em()
        
        if market_data is not None and not market_data.empty:
            # 计算市场摘要
            total_stocks = len(market_data)
            avg_change = market_data['涨跌幅'].mean()
            total_volume = market_data['成交量'].sum()
            total_turnover = market_data['成交额'].sum()
            
            # 获取涨跌家数
            up_stocks = len(market_data[market_data['涨跌幅'] > 0])
            down_stocks = len(market_data[market_data['涨跌幅'] < 0])
            
            summary = {
                'total_stocks': total_stocks,
                'average_change': round(avg_change, 2),
                'total_volume': int(total_volume) if pd.notna(total_volume) else 0,
                'total_turnover': float(total_turnover) if pd.notna(total_turnover) else 0,
                'up_stocks': up_stocks,
                'down_stocks': down_stocks,
                'timestamp': datetime.now().isoformat()
            }
            
            logger.info("获取市场数据摘要成功")
            return summary
        else:
            logger.warning("未获取到市场数据")
            return None
    except Exception as e:
        logger.error(f"获取市场数据摘要失败: {str(e)}")
        return None