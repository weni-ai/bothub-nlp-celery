import spacy
from celery import Celery
from kombu import Queue
from kombu.utils.objects import cached_property

from .actions import ACTION_PARSE
from .actions import ACTION_TRAIN
from .actions import ACTION_EVALUATE
from .actions import queue_name
from . import settings


class CeleryService(Celery):
    @cached_property
    def nlp_spacy(self):
        """Current nlp spacy instance."""
        print(f"loading {settings.BOTHUB_NLP_LANGUAGE_QUEUE} spacy lang model...")
        return spacy.load(settings.BOTHUB_NLP_LANGUAGE_QUEUE, parser=False)


celery_app = CeleryService(
    "bothub_nlp_celery",
    broker=settings.BOTHUB_NLP_CELERY_BROKER_URL,
    backend=settings.BOTHUB_NLP_CELERY_BACKEND_URL,
)


nlp_language = celery_app.nlp_spacy if settings.BOTHUB_NLP_SERVICE_WORKER else None


queues_name = set(
    [queue_name(ACTION_PARSE, lang) for lang in settings.SUPPORTED_LANGUAGES.keys()]
    + [queue_name(ACTION_TRAIN, lang) for lang in settings.SUPPORTED_LANGUAGES.keys()]
    + [
        queue_name(ACTION_EVALUATE, lang)
        for lang in settings.SUPPORTED_LANGUAGES.keys()
    ]
)
celery_app.conf.task_queues = [Queue(queue) for queue in queues_name]
