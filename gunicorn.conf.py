from multiprocessing import cpu_count
from pathlib import Path


Path("/var/log/gunicorn/").mkdir(parents=True, exist_ok=True)

errorlog = '/var/log/gunicorn/gunicorn.log'
loglevel = 'warning'
bind = 'unix:/opt/api/app.sock'
# Daemon turned off because of the note on the URL
# https://docs.gunicorn.org/en/latest/deploy.html#monitoring
daemon = False
workers = cpu_count() * 2 + 1
threads = 2
worker_class = 'uvicorn.workers.UvicornWorker'
# user = 'www-data'
# group = 'www-data'
