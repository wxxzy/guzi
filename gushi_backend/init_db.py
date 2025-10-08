import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db

def init_database():
    """初始化数据库"""
    app = create_app()
    
    with app.app_context():
        # 创建所有表
        db.create_all()
        print("数据库表创建成功!")
        
        # 同步股票列表
        from data_source.data_fetcher import sync_stock_list
        result = sync_stock_list()
        print(f"股票列表同步结果: {result}")

if __name__ == '__main__':
    init_database()