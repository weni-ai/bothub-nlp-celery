from setuptools import setup, find_packages


extras_requires = {
    "spacy": ["spacy>=2.1,<2.2"],
}

setup(
    name='bothub-nlp-celery',
    version='0.1.28',
    description='Bothub NLP Celery',
    packages=find_packages(),
    install_requires=[
        'celery==4.3.0',
        'python-decouple==3.3',
        'sentry-sdk==0.13.2',
        'numpy==1.18.1',
        'spacy==2.1.9',
        'vine~=1.3.0',
    ],
    extras_require=extras_requires,
)
