from setuptools import setup, find_packages


setup(
    name='bothub-nlp-celery',
    version='0.1.1',
    description='Bothub NLP Celery',
    packages=find_packages(),
    install_requires=[
        'celery==4.2.1',
        'python-decouple==3.1',
    ],
)
