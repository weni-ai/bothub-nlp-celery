import settings

ACTION_PARSE = "parse"
ACTION_DEBUG_PARSE = "debug_parse"
ACTION_SENTENCE_SUGGESTION = "sentence_suggestion"
ACTION_INTENT_SENTENCE_SUGGESTION = "intent_sentence_suggestion"
ACTION_WORD_SUGGESTION = "word_suggestion"
ACTION_WORDS_DISTIRBUTION = "words_distribution"
ACTION_SCORE_CALCULATION = "score_calculation"
ACTION_TRAIN = "train"
ACTION_EVALUATE = "evaluate"

available_models_to_lang = {
    "BERT": settings.AVAILABLE_BERT_MODELS,
    "QA": settings.AVAILABLE_QA_MODELS,
    "SPACY": settings.AVAILABLE_SPACY_MODELS,
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
        # QUEUES_APPART_FROM_MULTILANG allows to handle separate queues for specific languages
        # sometimes it is needed to handle heavy load queues separately
        if language in settings.QUEUES_APPART_FROM_MULTILANG:
            queue = language
        else:
            queue = "multilang"

    return queue
