from multiprocessing import cpu_count
from pathlib import Path


Path("/var/log/gunicorn/").mkdir(parents=True, exist_ok=True)


pidfile = '/var/run/gunicorn.pid'
errorlog = '/var/log/gunicorn/gunicorn.log'
loglevel = 'warning'
bind = 'unix:/opt/api/app.sock'
daemon = False
workers = cpu_count() * 2 + 1
threads = 2
worker_class = '/usr/local/bin/uvicorn.workers.UvicornWorker'
user = 'www-data'
group = 'www-data'
