ACTION_PARSE = "parse"
ACTION_DEBUG_PARSE = "debug_parse"
ACTION_SENTENCE_SUGGESTION = "sentence_suggestion"
ACTION_INTENT_SENTENCE_SUGGESTION = "intent_sentence_suggestion"
ACTION_WORD_SUGGESTION = "word_suggestion"
ACTION_WORDS_DISTIRBUTION = "words_distribution"
ACTION_SCORE_CALCULATION = "score_calculation"
ACTION_TRAIN = "train"
ACTION_EVALUATE = "evaluate"


def queue_name(language, action=None, model_name=None):
    queue = language
    if model_name == "QA":
        if language not in ["en", "pt_br"]:
            queue = f"multilang-{model_name}"
        else:
            queue += f"-{model_name}"
    elif model_name is not None:
        queue += f"-{model_name}"
    return queue
