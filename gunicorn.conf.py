import multiprocessing
import os

WORKERS_DEFAULT = multiprocessing.cpu_count() * 2 + 1

workers = int(os.environ.get("WORKERS", WORKERS_DEFAULT))
errorlog = "-"
accesslog = "-"
access_log_format = '%({x-forwarded-for}i)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
