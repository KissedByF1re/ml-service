import os

loglevel = os.getenv("LOG_LEVEL", "INFO")
HOST = os.getenv("HOST", "0.0.0.0")
PORT = os.getenv("FE_PORT", "80")

bind = f"{HOST}:{PORT}"
timeout = 0
workers = 2
