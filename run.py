# run.py

from dotenv import load_dotenv
load_dotenv() # 加载.env文件中的环境变量

import os
from guzi_backend import create_app, db
from guzi_backend.models import Stock
from guzi_backend.services import data_service
from flask_migrate import Migrate

# 根据环境变量选择配置，默认为'development'
config_name = os.getenv('FLASK_CONFIG') or 'development'
app = create_app(config_name)

migrate = Migrate(app, db)

@app.cli.command('init-db')
def init_db_command():
    """运行数据库迁移以创建或更新表。"""
    # db.drop_all() # 在使用迁移时不再需要
    # db.create_all() # 在使用迁移时不再需要
    print('Running database upgrade...')
    # 调用flask db upgrade命令
    from flask.cli import current_app
    with current_app.app_context():
        from flask_migrate import upgrade
        upgrade()
    print('Database initialized/upgraded.')

@app.cli.command('update-stocks')
def update_stocks_command():
    """从数据源更新股票列表到数据库。"""
    with app.app_context():
        data_service.update_stock_list_in_db()

if __name__ == '__main__':
    # 启动开发服务器
    app.run(debug=True, port=5000)
