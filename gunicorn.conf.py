import multiprocessing
import os

WORKERS_DEFAULT = multiprocessing.cpu_count() * 2 + 1

workers = int(os.environ.get("WORKERS", WORKERS_DEFAULT))
