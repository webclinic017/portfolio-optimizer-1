import multiprocessing as mp
import os

bind = f"0.0.0.0:{os.getenv('PORT', 5000)}"
workers = os.getenv("WEB_CONCURRENCY", mp.cpu_count() * 2 + 1)
worker_class = "uvicorn.workers.UvicornWorker"
