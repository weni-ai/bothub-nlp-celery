from . import settings


ALGORITHM_TO_LANGUAGE_MODEL = {
    "neural_network_internal": None,
    "neural_network_external": "SPACY",
    "transformer_network_diet": None,
    "transformer_network_diet_word_embedding": "SPACY",
    "transformer_network_diet_bert": "BERT",
}


def get_algorithm_info():
    # todo: get data from config file / populate languages

    # Sorted by priority
    # last element -> default algorithm
    return [
        {
            "name": "transformer_network_diet_bert",
            "supported_languages": ["all"],
        },
        {"name": "transformer_network_diet_word_embedding", "supported_languages": []},
        {"name": "transformer_network_diet", "supported_languages": ["all"]},
    ]


def get_language_model(update):
    model = ALGORITHM_TO_LANGUAGE_MODEL[update.get("algorithm")]
    language = update.get("language")

    if model == "SPACY" and language not in settings.SPACY_LANGUAGES:
        model = None

    # Send parse to SPACY worker to use name_entities (only if BERT not in use)
    if (
        (update.get("use_name_entities"))
        and (model is None)
        and (language in settings.SPACY_LANGUAGES)
    ):
        model = "SPACY"

    return model


def choose_best_algorithm(language):
    supported_algorithms = get_algorithm_info()

    for model in supported_algorithms[:-1]:
        if language in model["supported_languages"]:
            return model["name"]

    # default algorithm
    return supported_algorithms[len(supported_algorithms) - 1]["name"]
