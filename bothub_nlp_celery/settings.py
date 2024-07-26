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

if BOTHUB_NLP_SENTRY_CLIENT:
    init(
        dsn=BOTHUB_NLP_SENTRY,
        environment=ENVIRONMENT,
        integrations=[CeleryIntegration()],
    )

# Input Arguments
PARSER.add_argument("--AIPLATFORM_LANGUAGE_QUEUE", type=str, default=None)
PARSER.add_argument("--AIPLATFORM_LANGUAGE_MODEL", type=str, default=None)

ARGUMENTS, _ = PARSER.parse_known_args()
AIPLATFORM_LANGUAGE_QUEUE = ARGUMENTS.AIPLATFORM_LANGUAGE_QUEUE
AIPLATFORM_LANGUAGE_MODEL = ARGUMENTS.AIPLATFORM_LANGUAGE_MODEL

BOTHUB_NLP_LANGUAGE_QUEUE = config("BOTHUB_NLP_LANGUAGE_QUEUE", default="en")
BOTHUB_LANGUAGE_MODEL = config("BOTHUB_LANGUAGE_MODEL", default=None)


# Time Limits
TASK_GENERAL_TIME_LIMIT = config("TASK_GENERAL_TIME_LIMIT", cast=int, default=120)
TASK_PARSE_TIME_LIMIT = config("TASK_PARSE_TIME_LIMIT", cast=int, default=10)

# Redis settings
REDIS_BACKEND_HEALTH_CHECK_INTERVAL = config(
    "REDIS_BACKEND_HEALTH_CHECK_INTERVAL", default=None
)
REDIS_SOCKET_CONNECT_TIMEOUT = config("REDIS_SOCKET_CONNECT_TIMEOUT", default=None)
REDIS_SOCKET_TIMEOUT = config("REDIS_SOCKET_TIMEOUT", cast=int, default=120)
REDIS_RETRY_ON_TIMEOUT = config("REDIS_RETRY_ON_TIMEOUT", cast=bool, default=False)
REDIS_SOCKET_KEEPALIVE = config("REDIS_SOCKET_KEEPALIVE", cast=bool, default=False)


def cast_language_list(ls):
    return [lang.strip() for lang in ls.split("|") if lang.strip()]


# Model settings
# Available SPACY models
AVAILABLE_SPACY_MODELS = config(
    "AVAILABLE_SPACY_MODELS", cast=cast_language_list, default="en|pt_br|es"
)
# Available BERT models
AVAILABLE_BERT_MODELS = config(
    "AVAILABLE_BERT_MODELS", cast=cast_language_list, default="en|pt_br|xx"
)
# Available QA models
AVAILABLE_QA_MODELS = config(
    "AVAILABLE_QA_MODELS", cast=cast_language_list, default="en|pt_br|xx"
)

# Queue settings
# Available languages with word2vec models
AVAILABLE_SPECIFIC_SPACY_QUEUES = config(
    "AVAILABLE_SPECIFIC_SPACY_QUEUES", cast=cast_language_list, default="en|pt_br|es"
)
# Available languages with BERT models
AVAILABLE_SPECIFIC_BERT_QUEUES = config(
    "AVAILABLE_SPECIFIC_BERT_QUEUES", cast=cast_language_list, default="en|pt_br"
)
# Available languages with QA models
AVAILABLE_SPECIFIC_QA_QUEUES = config(
    "AVAILABLE_SPECIFIC_QA_QUEUES", cast=cast_language_list, default="en|pt_br"
)
# Languages without model that need to be handled in exclusive queues
AVAILABLE_SPECIFIC_QUEUES = config(
    "AVAILABLE_SPECIFIC_QUEUES", cast=cast_language_list, default=""
)
