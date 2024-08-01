# Description: Gunicorn configuration file

# Load app pre-fork to save memory and worker startup time
preload_app = True

# Maximum number of requests a worker will process before restarting
max_requests = 5

# Maximum number jitter to add to max_requests
max_requests_jitter = 4

# Timeout for worker to process a request
timeout = 120

# Number of worker processes
workers = 2

# Host and port to bind
bind = "0.0.0.0:30000"
