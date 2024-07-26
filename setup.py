from setuptools import setup, find_packages

setup(
    name="bothub-nlp-celery",
    version="0.1.38",
    description="Bothub NLP Celery",
    packages=find_packages(),
    install_requires=[
        "celery==5.1.2",
        "python-decouple==3.3",
        "sentry-sdk==0.13.2",
    ],
)
