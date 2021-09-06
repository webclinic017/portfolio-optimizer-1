import multiprocessing as mp
import os

host = os.getenv("HOST", "0.0.0.0")
port = os.getenv("PORT", 5000)
bind = f"{host}:{port}"
workers = os.getenv("WEB_CONCURRENCY", mp.cpu_count() * 2 + 1)
worker_class = "uvicorn.workers.UvicornWorker"
