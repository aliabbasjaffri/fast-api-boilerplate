import shutil
from pathlib import Path
from multiprocessing import cpu_count


Path('/var/log/gunicorn/').mkdir(parents=True, exist_ok=True)
shutil.chown('/var/log/gunicorn/', user='www-data', group='www-data')

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
