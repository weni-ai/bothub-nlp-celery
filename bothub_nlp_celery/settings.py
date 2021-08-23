import argparse
from sentry_sdk import init
from sentry_sdk.integrations.celery import CeleryIntegration
from decouple import config

PARSER = argparse.ArgumentParser()

ENVIRONMENT = config("ENVIRONMENT", default="production")

BOTHUB_NLP_CELERY_BROKER_URL = config(
    "BOTHUB_NLP_CELERY_BROKER_URL", default="redis://localhost:6379/0"
)

BOTHUB_NLP_CELERY_BACKEND_URL = config(
    "BOTHUB_NLP_CELERY_BACKEND_URL", default=BOTHUB_NLP_CELERY_BROKER_URL
)


BOTHUB_NLP_SENTRY_CLIENT = config(
    "BOTHUB_NLP_CELERY_SENTRY_CLIENT", cast=bool, default=False
)

BOTHUB_NLP_SENTRY = config("BOTHUB_NLP_CELERY_SENTRY", default=None)

# Input Arguments
PARSER.add_argument("--AIPLATFORM_LANGUAGE_QUEUE", type=str, default=None)
PARSER.add_argument("--AIPLATFORM_LANGUAGE_MODEL", type=str, default=None)

ARGUMENTS, _ = PARSER.parse_known_args()
AIPLATFORM_LANGUAGE_QUEUE = ARGUMENTS.AIPLATFORM_LANGUAGE_QUEUE
AIPLATFORM_LANGUAGE_MODEL = ARGUMENTS.AIPLATFORM_LANGUAGE_MODEL

BOTHUB_NLP_SERVICE_WORKER = config(
    "BOTHUB_NLP_SERVICE_WORKER", cast=bool, default=False
)

GOOGLE_APPLICATION_CREDENTIALS = config("GOOGLE_APPLICATION_CREDENTIALS", default=None)

BOTHUB_NLP_LANGUAGE_QUEUE = config("BOTHUB_NLP_LANGUAGE_QUEUE", default="en")
BOTHUB_LANGUAGE_MODEL = config("BOTHUB_LANGUAGE_MODEL", default=None)

SPACY_LANGUAGES = ["en", "pt_br", "es", "fr", "ru"]

BERT_LANGUAGES = ["pt_br", "en"]

if BOTHUB_NLP_SENTRY_CLIENT:
    init(
        dsn=BOTHUB_NLP_SENTRY,
        environment=ENVIRONMENT,
        integrations=[CeleryIntegration()],
    )

# Time Limits
TASK_GENERAL_TIME_LIMIT = config("TASK_GENERAL_TIME_LIMIT", cast=int, default=120)
TASK_PARSE_TIME_LIMIT = config("TASK_PARSE_TIME_LIMIT", cast=int, default=10)

# Redis settings
REDIS_BACKEND_HEALTH_CHECK_INTERVAL = config("REDIS_BACKEND_HEALTH_CHECK_INTERVAL", default=None)
REDIS_SOCKET_CONNECT_TIMEOUT = config("REDIS_SOCKET_CONNECT_TIMEOUT", default=None)
REDIS_SOCKET_TIMEOUT = config("REDIS_SOCKET_TIMEOUT", cast=int, default=120)
REDIS_RETRY_ON_TIMEOUT = config("REDIS_RETRY_ON_TIMEOUT", cast=bool, default=False)
REDIS_SOCKET_KEEPALIVE = config("REDIS_SOCKET_KEEPALIVE", cast=bool, default=False)
