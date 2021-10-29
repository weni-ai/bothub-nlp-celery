# Bothub NLP Celery Manager

This package abstracts and centralize all Bothub NLP Celery app features.

Usually this package is used as dependency in another packages.

## Environment Variables

### Connection variables
| Variable | Type | Default | Description |
|--|--|--|--|
| ENVIRONMENT | `string` | `production` |  |
| BOTHUB_NLP_CELERY_BROKER_URL | `string` | `redis://localhost:6379/0` | Celery Broker URL, check usage instructions in [Celery Docs](http://docs.celeryproject.org/en/latest/index.html) |
| BOTHUB_NLP_CELERY_BACKEND_URL | `string` | `BOTHUB_NLP_CELERY_BROKER_URL` value | Celery Backend URL, check usage instructions in [Celery Docs](http://docs.celeryproject.org/en/latest/index.html) |
| BOTHUB_NLP_CELERY_SENTRY_CLIENT | `boolean` | `False` | Enable Sentry |
| BOTHUB_NLP_CELERY_SENTRY | `str` | `None` | Set URL Sentry Server |

### AI Platform arguments

| Variable | Type | Default | Description |
|--|--|--|--|
| AIPLATFORM_LANGUAGE_QUEUE | `string` | `None` | Language prefix |
| AIPLATFORM_LANGUAGE_MODEL | `string` | `None` | Model type |

### Celery worker model variables
Variables that will be used by the worker nodes

| Variable | Type | Default | Description |
|--|--|--|--|
| BOTHUB_NLP_LANGUAGE_QUEUE | `string` | `en` | Set language of model that will be loaded in celery and will define its queue|
| BOTHUB_LANGUAGE_MODEL | `string` | `None` | Set type of model |
| TASK_GENERAL_TIME_LIMIT | `int` | `120` | Time limit of celery tasks |
| TASK_PARSE_TIME_LIMIT | `int` | `10` | Time limit of parse task |

### Celery queue variables
Variables that will be used by both the worker and the application that send the tasks

| Variable | Type | Default | Description |
|--|--|--|--|
| AVAILABLE_SPACY_MODELS | `string` | <code>en&#124;pt_br&#124;es&#124;fr&#124;ru</code> | Available SPACY models of working nodes |
| AVAILABLE_BERT_MODELS | `string` | <code>en&#124;pt_br&#124;xx</code> | Available BERT models of working nodes |
| AVAILABLE_QA_MODELS | `string` | <code>en&#124;pt_br&#124;xx</code> | Available QA models of working nodes |
| AVAILABLE_SPECIFIC_SPACY_QUEUES | `string` | <code>en&#124;pt_br&#124;es&#124;fr&#124;ru</code> | Available languages with word2vec models |
| AVAILABLE_SPECIFIC_BERT_QUEUES | `string` | <code>en&#124;pt_br</code> | Available languages with BERT models |
| AVAILABLE_SPECIFIC_QA_QUEUES | `string` | <code>en&#124;pt_br</code> | Available languages with QA models |
| AVAILABLE_SPECIFIC_QUEUES | `string` | `""` | Languages without model that need to be handled in exclusive queues |
