from googleapiclient import discovery
from googleapiclient import errors
from . import settings


ACTION_PARSE = "parse"
ACTION_DEBUG_PARSE = "debug_parse"
ACTION_SENTENCE_SUGGESTION = "sentence_suggestion"
ACTION_WORDS_DISTIRBUTION = "words_distribution"
ACTION_TRAIN = "train"
ACTION_EVALUATE = "evaluate"


def queue_name(action, language, model_name):
    if settings.BOTHUB_NLP_NLU_AGROUP_LANGUAGE_QUEUE:
        return language
    return "{}:{}:{}".format(action, language, model_name)
