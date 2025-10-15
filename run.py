# run.py

from guzi_backend import create_app

# 通过应用工厂创建app实例
app = create_app()

if __name__ == '__main__':
    # 启动开发服务器
    # 在生产环境中，应使用Gunicorn或uWSGI等WSGI服务器
    # 例如: gunicorn -w 4 -b 0.0.0.0:5000 "run:app"
    app.run(debug=True, port=5000)
