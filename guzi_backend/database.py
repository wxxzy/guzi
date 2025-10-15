# guzi_backend/database.py

from flask_sqlalchemy import SQLAlchemy

# 创建一个SQLAlchemy实例，但不与任何应用关联
# 应用实例将在应用工厂中进行关联
db = SQLAlchemy()
