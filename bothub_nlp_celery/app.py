import numpy as np
import os

from celery import Celery
from kombu import Queue
from kombu.utils.objects import cached_property

from .actions import ACTION_PARSE
from .actions import ACTION_DEBUG_PARSE
from .actions import ACTION_SENTENCE_SUGGESTION
from .actions import ACTION_TRAIN
from .actions import ACTION_EVALUATE
from .actions import queue_name
from . import settings


class CeleryService(Celery):
    @cached_property
    def nlp_spacy(self):
        """Current nlp spacy instance."""
        import spacy

        print(f"loading {settings.BOTHUB_NLP_LANGUAGE_QUEUE} spacy lang model...")
        nlp = spacy.load(settings.BOTHUB_NLP_LANGUAGE_QUEUE, parser=False)
        if nlp.vocab.vectors_length >= 0:
            norms = np.linalg.norm(nlp.vocab.vectors.data, axis=1, keepdims=True)
            norms[norms == 0] = 1
            nlp.vocab.vectors.data /= norms
        return nlp

    @cached_property
    def nlp_bert(self):
        print(f"loading {settings.BOTHUB_NLP_LANGUAGE_QUEUE} bert lang model...")

        from bothub_nlp_rasa_utils.pipeline_components.registry import (
            model_class_dict,
            from_pt_dict,
            model_weights_defaults,
            model_tokenizer_dict,
            language_to_model
        )

        model_name = language_to_model[settings.BOTHUB_NLP_LANGUAGE_QUEUE]

        bert_tokenizer = model_tokenizer_dict[model_name].from_pretrained(
            model_weights_defaults[model_name], cache_dir=None
        )

        # This is a path fix for unit tests
        cur_dir = os.getcwd()
        print(cur_dir)
        cur_dir = cur_dir.split("/")[-1]
        if cur_dir == "tests":
            os.chdir("../")

        bert_model = model_class_dict[model_name].from_pretrained(
            model_name, cache_dir=None,
            from_pt=from_pt_dict.get(model_name, False)
        )

        return bert_tokenizer, bert_model


celery_app = CeleryService(
    "bothub_nlp_celery",
    broker=settings.BOTHUB_NLP_CELERY_BROKER_URL,
    backend=settings.BOTHUB_NLP_CELERY_BACKEND_URL,
)

print(os.environ.get('BOTHUB_LANGUAGE_MODEL'))
nlp_tokenizer = None
if settings.BOTHUB_LANGUAGE_MODEL == "SPACY":
    nlp_language = celery_app.nlp_spacy if settings.BOTHUB_NLP_SERVICE_WORKER else None
elif settings.AIPLATFORM_LANGUAGE_MODEL == "SPACY":
    import spacy
    nlp_language = spacy.load(settings.AIPLATFORM_LANGUAGE_QUEUE, parser=False)
elif settings.BOTHUB_LANGUAGE_MODEL == "BERT":
    nlp_language = celery_app.nlp_bert
else:
    nlp_language = None


queues_name = set()
for lang in settings.SUPPORTED_LANGUAGES.keys():
    queues_name.add(queue_name(lang, ACTION_PARSE))
    queues_name.add(queue_name(lang, ACTION_DEBUG_PARSE))
    queues_name.add(queue_name(lang, ACTION_SENTENCE_SUGGESTION))
    queues_name.add(queue_name(lang, ACTION_TRAIN))
    queues_name.add(queue_name(lang, ACTION_EVALUATE))
    for language_model in settings.SUPPORTED_LANGUAGE_MODELS.keys():
        queues_name.add(queue_name(lang, ACTION_PARSE, language_model))
        queues_name.add(queue_name(lang, ACTION_DEBUG_PARSE, language_model))
        queues_name.add(queue_name(lang, ACTION_SENTENCE_SUGGESTION, language_model))
        queues_name.add(queue_name(lang, ACTION_TRAIN, language_model))
        queues_name.add(queue_name(lang, ACTION_EVALUATE, language_model))

celery_app.conf.task_queues = [Queue(queue) for queue in queues_name]
