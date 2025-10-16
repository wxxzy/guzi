# run.py

from dotenv import load_dotenv
load_dotenv() # 加载.env文件中的环境变量

import os
from guzi_backend import create_app, db
from guzi_backend.models import Stock
from guzi_backend.services import data_service

# 根据环境变量选择配置，默认为'development'
config_name = os.getenv('FLASK_CONFIG') or 'development'
app = create_app(config_name)

@app.cli.command('init-db')
def init_db_command():
    """清除现有数据并创建新表。"""
    db.create_all()
    print('Initialized the database.')

@app.cli.command('update-stocks')
def update_stocks_command():
    """从数据源更新股票列表到数据库。"""
    with app.app_context():
        data_service.update_stock_list_in_db()

if __name__ == '__main__':
    # 启动开发服务器
    app.run(debug=True, port=5000)
