from multiprocessing import cpu_count


def max_workers():
    return cpu_count()


pidfile = '/tmp/hello-http-unix.pid'
errorlog = '/var/log/gunicorn/gunicorn.log'
loglevel = 'warning'
bind = 'unix:/opt/api/app.sock'
daemon = False
workers = max_workers()
threads = 2
worker_class = '/usr/local/bin/uvicorn.workers.UvicornWorker'
user = 'www-data'
group = 'www-data'
