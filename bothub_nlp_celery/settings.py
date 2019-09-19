import environ
from collections import OrderedDict


def cast_supported_languages(i):
    return OrderedDict([
        x.split(':', 1) if ':' in x else (x, x) for x in
        i.split('|')
    ])


environ.Env.read_env(env_file=(environ.Path(__file__) - 2)('.env'))

env = environ.Env(
    # set casting, default value
    BOTHUB_NLP_CELERY_BROKER_URL=(str, 'redis://localhost:6379/0'),
    BOTHUB_NLP_NLU_AGROUP_LANGUAGE_QUEUE=(bool, True),
    BOTHUB_NLP_DEBUG=(bool, False),
    BOTHUB_NLP_SENTRY_CLIENT=(bool, None),
    SUPPORTED_LANGUAGES=(cast_supported_languages, 'en|pt'),
)


BOTHUB_NLP_CELERY_BROKER_URL = env.str('BOTHUB_NLP_CELERY_BROKER_URL',)

BOTHUB_NLP_CELERY_BACKEND_URL = env.str(
    'BOTHUB_NLP_CELERY_BACKEND_URL',
    default=BOTHUB_NLP_CELERY_BROKER_URL,
)

BOTHUB_NLP_NLU_AGROUP_LANGUAGE_QUEUE = env.bool(
    'BOTHUB_NLP_NLU_AGROUP_LANGUAGE_QUEUE'
)

BOTHUB_NLP_DEBUG = env.bool(
    'BOTHUB_NLP_DEBUG'
)

BOTHUB_NLP_DEVELOPMENT_MODE = env.bool(
    'BOTHUB_NLP_DEVELOPMENT_MODE',
    default=BOTHUB_NLP_DEBUG
)

BOTHUB_NLP_SENTRY_CLIENT = env.bool(
    'BOTHUB_NLP_SENTRY_CLIENT'
)

SUPPORTED_LANGUAGES = env.get_value(
    'SUPPORTED_LANGUAGES',
    cast_supported_languages,
    'en|pt',
    True
)
