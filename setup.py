from setuptools import setup, find_packages


setup(
    name='bothub-nlp-celery',
    version='0.1.4',
    description='Bothub NLP Celery',
    packages=find_packages(),
    install_requires=[
        'celery==4.3.0',
        'python-decouple==3.1',
        'spacy==2.0.18',
    ],
)
