import numpy as np
import spacy

from celery import Celery
from kombu import Queue
from kombu.utils.objects import cached_property

from .actions import ACTION_PARSE
from .actions import ACTION_DEBUG_PARSE
from .actions import ACTION_SENTENCE_SUGGESTION
from .actions import ACTION_WORDS_DISTIRBUTION
from .actions import ACTION_TRAIN
from .actions import ACTION_EVALUATE
from .actions import queue_name
from . import settings


class CeleryService(Celery):
    @cached_property
    def nlp_spacy(self):
        """Current nlp spacy instance."""

        print(f"loading {settings.BOTHUB_NLP_LANGUAGE_QUEUE} spacy lang model...")
        nlp = spacy.load(settings.BOTHUB_NLP_LANGUAGE_QUEUE, parser=False)
        if nlp.vocab.vectors_length >= 0:
            norms = np.linalg.norm(nlp.vocab.vectors.data, axis=1, keepdims=True)
            norms[norms == 0] = 1
            nlp.vocab.vectors.data /= norms
        return nlp


    def nlp_bert(self):
        print(f"loading {settings.BOTHUB_NLP_LANGUAGE_QUEUE} bert lang model...")
        
        from bothub_nlp_rasa_utils.pipeline_components.registry import (
            model_class_dict,
            model_weights_defaults,
            model_tokenizer_dict,
        )

        tokenizer = model_tokenizer_dict[settings.BERT_MODEL_NAME].from_pretrained(
            model_weights_defaults[settings.BERT_MODEL_NAME], cache_dir=settings.BERT_CACHE_DIR
        )
        model = model_class_dict[settings.BERT_MODEL_NAME].from_pretrained(
            model_weights_defaults[settings.BERT_MODEL_NAME], cache_dir=settings.BERT_CACHE_DIR
        )


celery_app = CeleryService(
    "bothub_nlp_celery",
    broker=settings.BOTHUB_NLP_CELERY_BROKER_URL,
    backend=settings.BOTHUB_NLP_CELERY_BACKEND_URL,
)


# nlp_language = (
#     spacy.load(settings.BOTHUB_NLP_LANGUAGE_QUEUE, parser=False)
#     if settings.BOTHUB_NLP_AI_PLATFORM
#     else (celery_app.nlp_spacy if settings.BOTHUB_NLP_SERVICE_WORKER else None)
# )


if settings.BOTHUB_NLP_AI_PLATFORM and BOTHUB_LANGUAGE_MODEL == "SPACY":
    nlp_language = spacy.load(settings.BOTHUB_NLP_LANGUAGE_QUEUE, parser=False)
elif BOTHUB_LANGUAGE_MODEL == "SPACY":
    nlp_language = (celery_app.nlp_spacy if settings.BOTHUB_NLP_SERVICE_WORKER else None)
elif settings.BOTHUB_NLP_AI_PLATFORM and BOTHUB_LANGUAGE_MODEL == "BERT":
    nlp_language = celery_app.nlp_bert()
else:
    nlp_language = None

queues_name = set(
    [queue_name(ACTION_PARSE, lang) for lang in settings.SUPPORTED_LANGUAGES.keys()]
    + [
        queue_name(ACTION_DEBUG_PARSE, lang)
        for lang in settings.SUPPORTED_LANGUAGES.keys()
    ]
    + [
        queue_name(ACTION_SENTENCE_SUGGESTION, lang)
        for lang in settings.SUPPORTED_LANGUAGES.keys()
    ]
    + [queue_name(ACTION_TRAIN, lang) for lang in settings.SUPPORTED_LANGUAGES.keys()]
    + [
        queue_name(ACTION_EVALUATE, lang)
        for lang in settings.SUPPORTED_LANGUAGES.keys()
    ]
)
celery_app.conf.task_queues = [Queue(queue) for queue in queues_name]
