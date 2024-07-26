from celery import Celery
from kombu.utils.objects import cached_property

from . import settings, celeryconfig

import logging

logger = logging.getLogger(__name__)


class CeleryService(Celery):
    @cached_property
    def nlp_bert(self):
        logger.info(f"loading {settings.BOTHUB_NLP_LANGUAGE_QUEUE} bert lang model...")

        from bothub.shared.utils.rasa_components.registry import (
            model_class_dict,
            from_pt_dict,
            model_weights_defaults,
            model_tokenizer_dict,
            language_to_model,
        )

        model_name = language_to_model[settings.BOTHUB_NLP_LANGUAGE_QUEUE]

        bert_tokenizer = model_tokenizer_dict[model_name].from_pretrained(
            model_weights_defaults[model_name], cache_dir=None
        )

        bert_model = model_class_dict[model_name].from_pretrained(
            model_name, cache_dir=None, from_pt=from_pt_dict.get(model_name, False)
        )

        return bert_tokenizer, bert_model

    @cached_property
    def qa_model(self):
        """
        Must be called from question-answering module
        :return: Loaded cached QA-MODELS
        """
        from utils import model_info
        from simpletransformers.question_answering import QuestionAnsweringModel

        logger.info(f"Loading QA models...")

        models = {}

        for model in settings.AVAILABLE_QA_MODELS:
            model_data = model_info.get(model)
            try:
                models[model] = QuestionAnsweringModel(
                    model_data.get("type"),
                    model_data.get("dir"),
                    args=model_data.get("args"),
                    use_cuda=True,
                )
            except ValueError as err:
                logger.debug(err)
                models[model] = QuestionAnsweringModel(
                    model_data.get("type"),
                    model_data.get("dir"),
                    args=model_data.get("args"),
                    use_cuda=False,
                )

        return models


celery_app = CeleryService("bothub_nlp_celery")
celery_app.config_from_object(celeryconfig)

if settings.BOTHUB_LANGUAGE_MODEL == "BERT":
    nlp_language = celery_app.nlp_bert
else:
    nlp_language = None
