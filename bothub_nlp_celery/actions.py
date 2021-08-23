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
    if model_name == "SPACY":
        if language == "pt_br" and action in [ACTION_SENTENCE_SUGGESTION, ACTION_INTENT_SENTENCE_SUGGESTION, ACTION_WORD_SUGGESTION]:
            queue = "pt_br-SPACY_SUGGESTION"
        elif language in ["en", "pt_br", "es", "ru", "fr", "pt"]:
            queue = language + "-SPACY"
        else:
            queue = "multilang"
    elif model_name is not None:
        if language in ["en", "pt_br"]:
            queue = language + "-" + model_name
        else:
            queue = "multilang-" + model_name
    else:
        if language in ["en", "pt_br"]:
            queue = language
        else:
            queue = "multilang"

    return queue

#
# def queue_name(language, action=None, model_name=None):
#     queue = language
#     if model_name == "QA":
#         if language not in ["en", "pt_br"]:
#             queue = f"multilang-{model_name}"
#         else:
#             queue += f"-{model_name}"
#     elif model_name is not None:
#         queue += f"-{model_name}"
#     return queue
