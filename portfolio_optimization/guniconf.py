import multiprocessing as mp
import os

bind = "0.0.0.0:5000"
workers = os.getenv("WEB_CONCURRENCY", mp.cpu_count() * 2 + 1)
worker_class = "uvicorn.workers.UvicornWorker"
