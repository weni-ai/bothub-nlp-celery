from bothub_nlp_celery import settings, tasks

# Broker / Backend configuration
broker_url = settings.BOTHUB_NLP_CELERY_BROKER_URL
result_backend = settings.BOTHUB_NLP_CELERY_BACKEND_URL

# Tasks configuration
task_annotations = {
    tasks.TASK_NLU_PARSE_TEXT: {"time_limit": settings.TASK_PARSE_TIME_LIMIT},
    tasks.TASK_NLU_TRAIN_UPDATE: {"time_limit": float('inf')},
}
task_time_limit = settings.TASK_GENERAL_TIME_LIMIT

# Redis configuration

# The Redis backend supports health checks.
# This value must be set as an integer whose value is the number of seconds between health checks.
# If a ConnectionError or a TimeoutError is encountered during the health check,
# the connection will be re-established and the command retried exactly once.
redis_backend_health_check_interval = settings.REDIS_BACKEND_HEALTH_CHECK_INTERVAL

# Socket timeout for connections to Redis from the result backend in seconds (int/float)
redis_socket_connect_timeout = settings.REDIS_SOCKET_CONNECT_TIMEOUT

# Socket timeout for reading/writing operations to the Redis server in seconds (int/float),
# used by the redis result backend.
redis_socket_timeout = settings.REDIS_SOCKET_TIMEOUT

# To retry reading/writing operations on TimeoutError to the Redis server, used by the redis result backend.
# Shouldn’t set this variable if using Redis connection by unix socket.
redis_retry_on_timeout = settings.REDIS_RETRY_ON_TIMEOUT

# Socket TCP keepalive to keep connections healthy to the Redis server, used by the redis result backend.
redis_socket_keepalive = settings.REDIS_SOCKET_KEEPALIVE
