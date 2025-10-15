# app.py

from flask import Flask, jsonify

# 初始化Flask应用
app = Flask(__name__)

@app.route('/')
def index():
    """根路径，用于健康检查或欢迎页面。"""
    return "Welcome to the Stock Analysis System Backend!"

@app.route('/api/v1')
def api_base():
    """API基础路径，返回API信息。"""
    return jsonify({
        "code": 0,
        "message": "Success",
        "data": {
            "service": "Stock Analysis API",
            "version": "v1"
        }
    })

if __name__ == '__main__':
    # 启动开发服务器
    # 在生产环境中，应使用Gunicorn或uWSGI等WSGI服务器
    app.run(debug=True, port=5000)
