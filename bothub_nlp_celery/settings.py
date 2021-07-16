import argparse
from sentry_sdk import init
from sentry_sdk.integrations.celery import CeleryIntegration
from decouple import config
#from collections import OrderedDict

#
# def cast_supported_languages(i):
#     return OrderedDict([x.split(":", 1) if ":" in x else (x, x) for x in i.split("|")])
#

PARSER = argparse.ArgumentParser()

ENVIRONMENT = config("ENVIRONMENT", default="production")

BOTHUB_NLP_CELERY_BROKER_URL = config(
    "BOTHUB_NLP_CELERY_BROKER_URL", default="redis://localhost:6379/0"
)

BOTHUB_NLP_CELERY_BACKEND_URL = config(
    "BOTHUB_NLP_CELERY_BACKEND_URL", default=BOTHUB_NLP_CELERY_BROKER_URL
)

# BOTHUB_NLP_NLU_AGROUP_LANGUAGE_QUEUE = config(
#     "BOTHUB_NLP_NLU_AGROUP_LANGUAGE_QUEUE", cast=bool, default=True
# )

BOTHUB_NLP_SENTRY_CLIENT = config(
    "BOTHUB_NLP_CELERY_SENTRY_CLIENT", cast=bool, default=False
)

BOTHUB_NLP_SENTRY = config("BOTHUB_NLP_CELERY_SENTRY", default=None)

# SUPPORTED_LANGUAGES = config(
#     "SUPPORTED_LANGUAGES", default="en|pt", cast=cast_supported_languages
# )

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

# BOTHUB_NLP_AI_PLATFORM = config("BOTHUB_NLP_AI_PLATFORM", cast=bool, default=False)

# BERT_MODEL_NAME = config("BERT_MODEL_NAME", default="bert_portuguese")

# SUPPORTED_LANGUAGE_MODELS = config(
#     "SUPPORTED_LANGUAGE_MODELS", default="SPACY|BERT", cast=cast_supported_languages
# )

BOTHUB_NLP_LANGUAGE_QUEUE = config("BOTHUB_NLP_LANGUAGE_QUEUE", default="en")
BOTHUB_LANGUAGE_MODEL = config("BOTHUB_LANGUAGE_MODEL", default=None)

SPACY_LANGUAGES = ["en", "pt_br", "xx", "es", "fr", "ru"]

BERT_LANGUAGES = ["pt_br", "en"]

if BOTHUB_NLP_SENTRY_CLIENT:
    init(
        dsn=BOTHUB_NLP_SENTRY,
        environment=ENVIRONMENT,
        integrations=[CeleryIntegration()],
    )
