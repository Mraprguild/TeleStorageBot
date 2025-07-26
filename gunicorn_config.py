"""
Gunicorn configuration for production webhook deployment
"""

import os

# Server socket
bind = f"0.0.0.0:{os.getenv('PORT', 5000)}"
backlog = 2048

# Worker processes
workers = 2
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Restart workers
max_requests = 1000
max_requests_jitter = 50
preload_app = True

# Logging
accesslog = "access.log"
errorlog = "error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = 'telegram-file-storage-webhook'

# Server mechanics
daemon = False
pidfile = '/tmp/telegram-webhook.pid'
user = None
group = None
tmp_upload_dir = None