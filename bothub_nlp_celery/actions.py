from . import settings

ACTION_PARSE = "parse"
ACTION_DEBUG_PARSE = "debug_parse"
ACTION_SENTENCE_SUGGESTION = "sentence_suggestion"
ACTION_INTENT_SENTENCE_SUGGESTION = "intent_sentence_suggestion"
ACTION_WORD_SUGGESTION = "word_suggestion"
ACTION_WORDS_DISTIRBUTION = "words_distribution"
ACTION_SCORE_CALCULATION = "score_calculation"
ACTION_TRAIN = "train"
ACTION_EVALUATE = "evaluate"
ACTION_QUESTION_ANSWERING = "question_answering"


available_models_to_lang = {
    "BERT": settings.AVAILABLE_SPECIFIC_BERT_QUEUES,
    "QA": settings.AVAILABLE_SPECIFIC_QA_QUEUES,
    "SPACY": settings.AVAILABLE_SPECIFIC_SPACY_QUEUES,
}


def queue_name(language, action=None, model_name=None):
    if (
        model_name == "SPACY"
        and language in ["pt_br", "pt"]
        and action
        in [
            ACTION_SENTENCE_SUGGESTION,
            ACTION_INTENT_SENTENCE_SUGGESTION,
            ACTION_WORD_SUGGESTION,
        ]
    ):  # Specific case of word_suggestion wang2vec Portuguese model
        queue = language + "-SPACY_SUGGESTION"
    elif model_name in available_models_to_lang:
        if language in available_models_to_lang.get(model_name):
            queue = language + "-" + model_name
        else:
            queue = "multilang-" + model_name
    else:
        # AVAILABLE_SPECIFIC_QUEUES allows to handle separate queues for specific languages
        # sometimes it is needed to handle heavy load queues separately
        if language in settings.AVAILABLE_SPECIFIC_QUEUES:
            queue = language
        else:
            queue = "multilang"

    return queue
