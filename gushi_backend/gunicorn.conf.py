# Gunicorn配置文件
import multiprocessing

# 服务器套接字
bind = "0.0.0.0:5000"

# 工作进程数
workers = multiprocessing.cpu_count() * 2 + 1

# 工作进程类
worker_class = "sync"

# 工作进程超时时间（秒）
timeout = 120

# 重启工作进程前的最大请求数
max_requests = 1000

# 重启工作进程前最大请求数的抖动范围
max_requests_jitter = 100

# 日志级别
loglevel = "info"

# 访问日志文件
accesslog = "/var/log/gushi/access.log"

# 错误日志文件
errorlog = "/var/log/gushi/error.log"

# 启用访问日志
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# 前台运行（用于调试）
# daemon = False

# 进程名称
proc_name = "gushi"

# PID文件
pidfile = "/var/run/gushi/gushi.pid"

# 用户和组（生产环境应设置为非root用户）
# user = "gushi"
# group = "gushi"

# 工作目录
# chdir = "/app"

# 预加载应用
preload_app = True

# 优雅关闭超时时间
graceful_timeout = 30

# 保持连接的超时时间
keepalive = 5